import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

CONSUMER_KEY = '8xgvjM815XpgrG5m0j7YUGTeh'
CONSUMER_SECRET = '6NXXgPlHYmGS8WXJgjvNOzifBCSt1QEjKT1PIVIvbDk0c4XSCG'
ACCESS_TOKEN = '126872677-67m9rPipKqKWN3Y8sVlWU6osOsLHD33WTlWhWoYb'
ACCESS_TOKEN_SECRET = 'u85vw1W4rI65fyvahJHQg7RGtYKo3j21xv3RtFGXUtmex'


auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            counter = 0
            with open('football_and_teams.json', 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=[
    'manchester united', 'man utd', 'mufc',
    'manunited',
    'arsenal', 'afc',
    'lfc', 'liverpool',
    'chelsea', 'cfc',
    'mancity', 'manchester city'])