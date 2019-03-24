import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd

def process_tweets(tweet):
    nltk_tokens = nltk.word_tokenize(tweet)  #token
    nltk_stopwords = stopwords.words('english')  #stopwords
    lemmatizer = WordNetLemmatizer() #lemmatizer

    print(nltk_tokens)


data = pd.read_json('football_and_teams.json', lines=True)
for line in data.text:
    process_tweets(line)

