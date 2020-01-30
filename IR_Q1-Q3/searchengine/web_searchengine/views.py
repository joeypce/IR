from django.shortcuts import render
import pandas as pd
import time
import re
import crawl.view_functions as vf
from textblob import TextBlob
from datetime import datetime, timezone
import pytz

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
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

def post_request_method(start_time ,mylist, mysort, myti):
    result = vf.searchfootballteam(mylist, mysort)
    rowlist = result['result']['docs']

    positive_list = 0
    negative_list = 0
    neutral_list = 0
    print(str(len(rowlist)))
    total_records = len(rowlist)
    for tweet in rowlist:
        # print(tweet['text'])
        analysis = TextBlob(clean_tweet(''.join(tweet['text'])))
        if analysis.sentiment.polarity > 0:
            tweet['sentiment'] = 'positive'
            positive_list = positive_list + 1
            # print('positive')
        elif analysis.sentiment.polarity == 0:
            tweet['sentiment'] = 'neutral'
            neutral_list = neutral_list + 1
            # print('neutral')
        else:
            tweet['sentiment'] = 'negative'
            negative_list = negative_list + 1
            # print('negative')

        #convert utc to local
        utc_time = str(''.join(tweet['created_at']))
        utc = datetime.strptime(utc_time,'%Y-%m-%dT%H:%M:%SZ')
        tweet['created_at'] = utc

        positive_perc = 0
        negative_perc = 0
        neutral_perc = 0

    if positive_list > 1:
        positive_perc = (positive_list / total_records) * 100
        negative_perc = (negative_list / total_records) * 100
        neutral_perc = (neutral_list / total_records) * 100
    else:
        positive_perc = 0
        negative_perc = 0
        neutral_perc = 0
    context = {
        'tweet_list': result['result'],
        'timetaken': 'Time taken to execute query: ' + str(round(time.time() - start_time, 2)) + ' seconds',
        'keyword': 'Results related to: ' + str(result['keyword']),

        #ascending or decending
        'current': mysort,
        'sort_list': sort_list,

        #text or image
        't_i_list': t_i_list,
        'current_t_i': myti,

        #sentimental analysis
        'positive_perc': positive_perc,
        'negative_perc': negative_perc,
        'neutral_perc': neutral_perc
    }

    return context
def searchengine_view(request):
    start_time = time.time()
    if request.method == 'POST':
        mysort = request.POST.get('dropdown')
        myti = request.POST['text_or_image']
        # mydate = request.POST['searchdate']
        print(myti)
        #  team and keyword querying
        if 'ManchesterUnited' in request.POST:
            mylist = ['manchesterunited', 'manutd', 'mufc', 'manunited']
            context = post_request_method(start_time, mylist, mysort, myti)
            return render(request, 'search_engine_website.html', context)

        elif 'Arsenal' in request.POST:
            mylist = ['arsenal', 'afc']
            context = post_request_method(start_time, mylist, mysort, myti)
            return render(request, 'search_engine_website.html', context)

        elif 'Liverpool' in request.POST:
            mylist = ['lfc', 'liverpool']
            context = post_request_method(start_time, mylist, mysort, myti)
            return render(request, 'search_engine_website.html', context)

        elif 'Chelsea' in request.POST:
            mylist = ['chelsea', 'cfc']
            context = post_request_method(start_time, mylist, mysort, myti)
            return render(request, 'search_engine_website.html', context)

        elif 'ManchesterCity' in request.POST:
            mylist = ['mancity', 'manchestercity']
            context = post_request_method(start_time, mylist, mysort, myti)
            return render(request, 'search_engine_website.html', context)

        elif 'searchbar' in request.POST:
            searchbartext = request.POST.get('searchbar_txt')
            mylist = []
            mylist.append(searchbartext)
            print(searchbartext)
            start_time = time.time()
            context = post_request_method(start_time, mylist, mysort, myti)
            return render(request, 'search_engine_website.html', context)

        elif 'btn_crawl' in request.POST:
            hashtag = request.POST.get('searchbar_txt')
            print(hashtag)
            context = vf.crawl_and_index(hashtag)
            return render(request, 'search_engine_website.html', context)
    else:

        context = {
            't_i_list': t_i_list,
            'sort_list': sort_list
        }
        return render(request, 'search_engine_website.html', context)

