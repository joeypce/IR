import pandas as pd

# keyword = {"manchester"}
data = pd.read_json('football_and_teams.json', lines=True)

list = []
tweetcounter = 0
for line in data.text:
    if "manchester" in line:
        list.append(tweetcounter)
    tweetcounter = tweetcounter + 1

print(list)

tweetText = []
for tweetindex in list:
    # print(tweetindex, ":", data.loc[tweetindex].text)
    tweetText.append(data.loc[tweetindex])

for e in tweetText:
    print(e.text)