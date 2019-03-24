from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

def searchengine_view(request):
    if request.method == 'POST':
        searchbartext = request.POST['searchbar']
        print(searchbartext)
        data = pd.read_json('crawl/football_and_teams.json', lines=True)

        ''' query keywords '''
        list = []
        tweetcounter = 0
        for line in data.text:
            if searchbartext in line:
                list.append(tweetcounter)
            tweetcounter = tweetcounter + 1

        print(list)

        tweetText = []
        for tweetindex in list:
            print(tweetindex, ":", data.loc[tweetindex].text)
            tweetText.append(data.loc[tweetindex])

        ''' end of query '''

        context = {
            'tweet_list': tweetText
        }

        print(list)

        return render(request, 'search_engine_website.html', context)
    else:
        return render(request, 'search_engine_website.html')

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

