//		Twitter		https://github.com/kurrik/twittergo
//		Twitter		https://github.com/ChimeraCoder/anaconda
//		Facebook	https://github.com/huandu/facebook
//		Tumblr		https://github.com/mattcunningham/gumblr
//		Instagram	https://github.com/yanatan16/golang-instagram
//		Reddit		https://github.com/jzelinskie/geddit
//		G+			https://godoc.org/google.golang.org/api/plus/v1
//		IRC			https://github.com/sorcix/irc

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/kurrik/oauth1a"
	"github.com/kurrik/twittergo"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"
)

type secret struct {
	AccessSecret string
	AccessToken  string
	ClientSecret string
	ClientToken  string
}

type Tweet struct {
	Account string
	Text    string
	Date    string
}

const (
	TZ         = "Europe/Moscow"
	FILE       = "tweets.yml"
	interval   = 5
	timeFormat = "2006-01-02 15:04"
)

var (
	client *twittergo.Client
	req    *http.Request
	resp   *twittergo.APIResponse
	tweet  *twittergo.Tweet
)

func LoadCredentials(account string) (c *twittergo.Client, err error) {
	var file = "settings-" + account + ".json"
	creds, err := ioutil.ReadFile(file)
	if err != nil {
		log.Printf("%v", err)
		return nil, err
	}
	var s secret
	err = json.Unmarshal(creds, &s)

	config := &oauth1a.ClientConfig{
		ConsumerKey:    s.ClientToken,
		ConsumerSecret: s.ClientSecret,
	}

	log.Printf("DEBUG: AccessSecret %v\n AccessToken %v\n", s.AccessSecret, s.AccessToken)
	log.Printf("DEBUG: ClientSecret %v\n ClientToken %v\n", s.ClientSecret, s.ClientToken)
	user := oauth1a.NewAuthorizedConfig(s.AccessToken, s.AccessSecret)
	client := twittergo.NewClient(config, user)
	return client, nil
}

func main() {

	flag.Usage = func() {
		fmt.Printf("twisource is a Twitter client with collaboration support.\n\n")
		fmt.Printf("Usage: twisource [options]\n\n")
		flag.PrintDefaults()
	}

	var mode = *flag.Bool("publish", false, "mode to publish tweets")
	flag.Parse()

	if mode {
		log.Printf("Mode is public.")
	}

	filename, _ := filepath.Abs(FILE)
	yamlFile, err := ioutil.ReadFile(filename)

	if err != nil {
		panic(err)
	}

	tweets := []Tweet{}

	err = yaml.Unmarshal(yamlFile, &tweets)
	if err != nil {
		log.Fatalf("error: %v", err)
	}

	now := time.Now()
	for _, t := range tweets {
		log.Printf(" Text %s\n", t.Text)
		log.Printf(" Account %s\n", t.Account)
		log.Printf(" Date %s\n", t.Date)
		sched, err := time.Parse(timeFormat, t.Date)
		if err != nil {
			log.Fatalf("error: %v", err)
		}
		if int64(sched.Sub(now).Minutes()) > 5 {
			log.Println("[DEBUG] Less than 5 min")
			client, err := LoadCredentials(t.Account)
			if err != nil {
				log.Printf("[DEBUG] Failed to load credentials: %v\n", err)
			}

			data := url.Values{}
			data.Set("status", fmt.Sprintf("Hello %v!", time.Now()))
			body := strings.NewReader(data.Encode())
			req, err = http.NewRequest("POST", "/1.1/statuses/update.json", body)
			if err != nil {
				fmt.Printf("Could not parse request: %v\n", err)
				os.Exit(1)
			}
			req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
			resp, err = client.SendRequest(req)
			if err != nil {
				fmt.Printf("Could not send request: %v\n", err)
				os.Exit(1)
			}

			tweet = &twittergo.Tweet{}
			err = resp.Parse(t.Text)
			if err != nil {
				if rle, ok := err.(twittergo.RateLimitError); ok {
					log.Printf("Rate limited, reset at %v\n", rle.Reset)
				} else if errs, ok := err.(twittergo.Errors); ok {
					for i, val := range errs.Errors() {
						fmt.Printf("Error #%v - ", i+1)
						fmt.Printf("Code: %v ", val.Code())
						fmt.Printf("Msg: %v\n", val.Message())
					}
				} else {
					fmt.Printf("Problem parsing response: %v\n", err)
				}
				os.Exit(1)
			}
		}
	}
}
