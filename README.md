OpenVZ SMM
==========

Allows updating status on Twitter from source file.

## Installation

- pip install -r requirements.txt
- add tweets to tweets.yml
- create files with account credentials
- make lint
- git commit -a
- git push

## Getting access tokens

Has to be done once.

1. Register your application via <https://apps.twitter.com/>.
2. Get your consumer and access tokens from
   <https://apps.twitter.com/app/[APP_ID]/keys>.
   Here you may have to confirm your phone number, only then Twitter will allow
   you to update statuses within an application.
3. Save `consumer_key`, `consumer_secret`, `access_token`,
   `access_token_secret`.

## Contacts

- [@OpenVZ](https://twitter.com/_openvz_)
- [@CRIU](https://twitter.com/__criu__)
- [@ProcessHauler](https://twitter.com/ProcessHauler)

## Similar tools

- [publishr](https://github.com/vti/publishr)
- [twty](https://github.com/mattn/twty)
