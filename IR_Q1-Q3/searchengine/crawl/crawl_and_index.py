#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import json
import time
import urllib.request as urllib2

# Twitter API credentials
CONSUMER_KEY = '8xgvjM815XpgrG5m0j7YUGTeh'
CONSUMER_SECRET = '6NXXgPlHYmGS8WXJgjvNOzifBCSt1QEjKT1PIVIvbDk0c4XSCG'
ACCESS_TOKEN = '126872677-67m9rPipKqKWN3Y8sVlWU6osOsLHD33WTlWhWoYb'
ACCESS_TOKEN_SECRET = 'u85vw1W4rI65fyvahJHQg7RGtYKo3j21xv3RtFGXUtmex'

# Create the api endpoint
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

# Mention the maximum number of tweets that you want to be extracted.

# maximum_number_of_tweets_to_be_extracted = \
#     int(input('Enter the number of tweets that you want to extract- '))

# Mention the hashtag that you want to look out for
hashtag = input('Enter the hashtag you want to scrape- ')

for tweet in tweepy.Cursor(api.search, q='#' + hashtag, rpp=100, lang='en', include_entities=True, since='2019-04-01').items(200):
    with open('tweets_with_hashtag_' + hashtag + '.json', 'a') as the_file:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            time.sleep(2)
            jsondata = {}
            jsondata['id'] = tweet.id
            jsondata['text'] = tweet.text
            jsondata['name'] = tweet.user.name
            jsondata['screen_name'] = tweet.user.screen_name
            jsondata['created_at'] = str(tweet.created_at)
            jsondata['lang'] = tweet.lang
            jsondata['favorite_count'] = tweet.favorite_count
            jsondata['retweet_count'] = tweet.retweet_count

            if 'media' in tweet.entities:
                for image in tweet.entities['media']:
                    jsondata['image_url'] = image['media_url']
            else:
                jsondata['image_url'] = 'null'

            y = json.dumps(jsondata)
            the_file.write(y)
            the_file.write("\n")

            print(y)

        url = 'http://localhost:8983/solr/testing/update/json?commit=true&wt=json'
        y = "[" + y + "]"
        y = y.encode("utf-8")
        req = urllib2.Request(url, y)
        req.add_header('Content-type', 'application/json')
        response = urllib2.urlopen(req)
        the_page = response.read()
        print(the_page.decode("utf-8"))


print('Extracted tweets with hashtag #' + hashtag)