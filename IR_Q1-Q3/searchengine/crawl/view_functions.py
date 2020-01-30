import pandas as pd
from textblob import TextBlob
import requests
import json
import re
import urllib
import tweepy
import json
import time
import urllib.request as urllib2

def searchfootballteam(keyword, order):
    if order == "impt":
        params = (
            ('q', 'text:' + '||'.join(keyword)),
            ('rows', '50')
        )
    else:
        params = (
            ('q', 'text:' + '||'.join(keyword)),
            ('rows', '50'),
            ('sort', 'created_at ' + order),
        )
    url = urllib.parse.urlencode(params)
    response = requests.get('http://localhost:8983/solr/footballtweets/select', params=params)
    result = response.json()["response"]
    # print(result)
    # data = pd.DataFrame(response.json()["response"]["docs"])
    # print(data)

    result_ = {
        'result': result,
        # 'json_url': str('http://localhost:8983/solr/footballtweets/select' + url)
        'keyword': keyword
    }
    return result_

    # data = pd.read_json('crawl/football_and_teams2(array).json', lines=True)
    # rowlist = []
    #
    # for counter in range(len(keyword)):
    #     for row, line in zip(data.index, data.text):
    #         if keyword[counter] in line:
    #             rowlist.append(row)
    #             # print(row)
    #
    # # ensure list has no duplicates
    # rowlist = list(dict.fromkeys(rowlist))
    # # print(rowlist)
    # tweetText = []
    # for tweetindex in rowlist:
    #     # print(tweetindex, ":", data.loc[tweetindex].text)
    #     analysis = TextBlob(clean_tweet(data.loc[tweetindex].text))
    #     if analysis.sentiment.polarity > 0:
    #         print('positive')
    #     elif analysis.sentiment.polarity == 0:
    #         print('neutral')
    #     else:
    #         print('negative')
    #     tweetText.append(data.loc[tweetindex])
    #
    # return tweetText

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())


def crawl_and_index(hashtag):
    # Twitter API credentials
    CONSUMER_KEY = '8xgvjM815XpgrG5m0j7YUGTeh'
    CONSUMER_SECRET = '6NXXgPlHYmGS8WXJgjvNOzifBCSt1QEjKT1PIVIvbDk0c4XSCG'
    ACCESS_TOKEN = '126872677-67m9rPipKqKWN3Y8sVlWU6osOsLHD33WTlWhWoYb'
    ACCESS_TOKEN_SECRET = 'u85vw1W4rI65fyvahJHQg7RGtYKo3j21xv3RtFGXUtmex'

    # Create the api endpoint
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth)

    print(hashtag)

    for tweet in tweepy.Cursor(api.search, q=hashtag, rpp=100, lang='en', include_entities=True).items(20):
        with open('tweets_with_hashtag_' + hashtag + '.json', 'a') as the_file:
            if (not tweet.retweeted) and ('RT @' not in tweet.text):
                time.sleep(1)
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

                url = 'http://localhost:8983/solr/footballtweets/update/json?commit=true&wt=json'
                y = "[" + y + "]"
                y = y.encode("utf-8")
                req = urllib2.Request(url, y)
                req.add_header('Content-type', 'application/json')
                response = urllib2.urlopen(req)
                the_page = response.read()
                print(the_page.decode("utf-8"))

    print('Extracted tweets with ' + hashtag)
    sort_list = [
        {
            'value_': 'impt',
            'text_': 'Importance'
        },
        {
            'value_': 'desc',
            'text_': 'Newest'
        },
        {
            'value_': 'asc',
            'text_': 'Oldest'
        }
    ]
    t_i_list = [
        {
            'value_': 'text',
            'text_': 'Text'
        },
        {
            'value_': 'img',
            'text_': 'Image'
        }
    ]
    context ={
        'crawl_result': 'Extracted tweets with ' + hashtag,
        # ascending or decending
        'sort_list': sort_list,

        # text or image
        't_i_list': t_i_list,
    }

    return context

