import pandas as pd

# data = pd.read_json('crawl/football_and_teams2.json', lines=True)
num_words = 0

fname = 'football_and_teams_final.json'
with open(fname, 'r') as f:
    for line in f:
        words = line.split()
        print(words)
        num_words += len(words)
print("Number of words:")
print(num_words)