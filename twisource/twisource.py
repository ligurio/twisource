#!/usr/bin/env python

# BSD license, Sergey Bronnikov

import argparse
import os
import re
import tweepy
from pytz import timezone
import datetime
import yaml
try:
    import json
except ImportError:
    import simplejson as json

tz = 'Europe/Moscow'
tweet_file = 'tweets.yml'


def lint(message, date, account):
    if len(message) > 140:
        print "[DEBUG] The text of your tweet scheduled at", date, "is too long"
        return 1
    return 0

    f = "settings-" + account + ".json"
    if not (os.path.isfile(f) and os.access(f, os.R_OK)):
        print "[DEBUG] File with credentials is not accessible"
        return 1
    return 0


def getRTid(message):
    m = re.match("^RT ([0-9]*)$", message)
    if m:
        return m.groups()[0]


def cred(account):
    f = "settings-" + account + ".json"
    with open(f) as fp:
        return json.load(fp)


def tweeter(message, account, mode):
    credentials = cred(account)
    auth = tweepy.OAuthHandler(credentials['ClientToken'], credentials['ClientSecret'])
    auth.set_access_token(credentials['AccessToken'], credentials['AccessSecret'])
    api = tweepy.API(auth)
    rt_id = getRTid(message)
    if rt_id:
        print "[DEBUG] %s: RT https://twitter.com/statuses/%s" % (account, rt_id)
    else:
        print "[DEBUG] %s: %s" % (account, message)
        if not rt_id:
            if mode:
                print "[DEBUG] Posting a message", message
                api.update_status(message)
                print "[DEBUG] Posted"
            else:
                if mode:
                    print "[DEBUG] Retweeting a message", rt_id
                    api.retweet(rt_id)
                    print "[DEBUG] Posted"


def main(mode):
    with open(tweet_file, 'r') as f:
        tweets = yaml.load(f)

    d = datetime.datetime.now(timezone(tz))
    print "[DEBUG] Time in timezone %s - %s" % (tz, d.strftime("%Y-%m-%d %H:%M"))
    for t in tweets:
        if t['date'] >= d.strftime("%Y-%m-%d %H:%M") and not lint(t['text'], t['date'], t['account']) and not mode:
            tweeter(t['text'], t['account'], mode)
            if t['date'] == d.strftime("%Y-%m-%d %H:%M") and not lint(t['text'], t['date'], t['account']) and mode:
                tweeter(t['text'], t['account'], mode)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post Twitter messages from file.')
    parser.add_argument("-p", "--publish", help="post scheduled messages", action='store_true')
    args = parser.parse_args()

    if args.publish:
        print "[DEBUG] publish mode enabled"
    else:
        print "[DEBUG] lint mode enabled"

    main(mode=args.publish)
