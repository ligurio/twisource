all: publish

publish: tweets.yml
	twisource.py --publish

lint: tweets.yml
	twisource.py --lint

.PHONY: all publish lint
