import pandas as pd

with open('tweets_with_hashtag_arsenal.json', encoding='utf-8-sig') as f_input:
    df = pd.read_json(f_input, lines=True)

df.to_csv('tweets_with_hashtag_arsenal.csv', encoding='utf-8', index=False)