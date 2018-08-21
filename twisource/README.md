<img width=150 src="tweets.png" align="right" />

Twisource
=========

- is a Twitter client. It allows you to update status on Twitter from source
file.

## Installation

- Install Python requirements

```
$ pip install -r requirements.txt
```

- Add tweets to tweets.yml.
- Create file(s) with account(s) credentials.
- Validate source file with scheduled tweets:

```
$ ./twisource
```

- Commit updated file and publish tweets:

```
$ git commit -a
$ git push
$ ./twisource --publish
```

## Getting access tokens

Has to be done once.

1. Register your application via <https://apps.twitter.com/>.
2. Get your consumer and access tokens from
   <https://apps.twitter.com/app/[APP_ID]/keys>.
   Here you may have to confirm your phone number, only then Twitter will allow
   you to update statuses within an application.
3. Save `consumer_key`, `consumer_secret`, `access_token`,
   `access_token_secret`.

## Users

- [OpenVZ, CRIU, P.Haul](https://www.openvz.org)
- ...

## Similar tools

- [publishr](https://github.com/vti/publishr)
- [twty](https://github.com/mattn/twty)

## Contacts

[sergeyb@](https://twitter.com/estet)
