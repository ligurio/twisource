#!/usr/bin/env python

# BSD license, Sergey Bronnikov

import argparse
import os
import re
import requests
import tweepy
import yaml
try:
        import json
except ImportError:
        import simplejson as json
from collections import defaultdict

tweet_file = 'tweets.yml'

def shorten(url):
	headers = {'content-type': 'application/json'}
	payload = {"longUrl": url}
	url = "https://www.googleapis.com/urlshortener/v1/url"
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	link = json.loads(r.text)['id']
	return link

def lint(message, date, account):
    if len(message) > 140:
       print "[DEBUG] The text of your tweet is too long"
       return 1
    return 0
	
    f = "settings-" + account + ".json"
    if not (os.path.isfile(f) and os.access(f, os.R_OK)):
       print "[DEBUG] File with credentials is not accessible"
       return 1
    return 0

def shorten(url):
    import urllib2
    fetcher = urllib2.urlopen('https://clck.ru/--?url='+ url)
    return fetcher.read()

def is_retweet(message):
    if not re.match("^RT [0-9]*$", message):
       print "[DEBUG] Simple message, not a retweet"
       return 1
    return 0

def cred(account):
    f = "settings-" + account + ".json"
    print "[DEBUG] Credential file", f
    settings = open(f).read()
    credentials = json.loads(settings)
    return credentials

def tweeter(message, account):
    credentials = cred(account)
    print "[DEBUG] Used Twitter account", account
    auth = tweepy.OAuthHandler(credentials['ClientToken'], credentials['ClientSecret'])
    auth.set_access_token(credentials['AccessToken'], credentials['AccessSecret'])
    api = tweepy.API(auth)
    if is_retweet(message):
       print "[DEBUG] Posting a message"
       print "[MESSAGE]", message
       #api.update_with_media(filename[, status][, source][, file])
       #api.update_status(post+" "+post_dict[post])
    else:
       print "[DEBUG] Retweet ID"
       #api.retweet(id)

def main():
    with open(tweet_file, 'r') as f:
         tweets = yaml.load(f)

    for t in tweets:
        print "[DEBUG]", t['date']
        if not lint(t['text'],t['date'],t['account']):
           tweeter(t['text'], t['account'])
        print "\n"
    f.close

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post Twitter messages from file.')
    parser.add_argument("-l", "--lint", help="validate scheduled messages", action='store_true')
    parser.add_argument("-p", "--publish", help="post scheduled messages", action='store_true')
    args = parser.parse_args()

    if args.lint:
       print "[DEBUG] lint"
    elif args.publish:
       print "[DEBUG] publish"

	#main()
