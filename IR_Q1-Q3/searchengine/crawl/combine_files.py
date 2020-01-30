import json

data = []
with open('tweets_with_hashtag_afc.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_arsenal.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_cfc.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_chelsea.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_lfc.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_liverpool.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_manchestercity.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_manchesterunited.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))
with open('tweets_with_hashtag_mancity.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_manunited.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_manutd.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

with open('tweets_with_hashtag_mufc.json', encoding="utf8") as f:
    for line in f:
        data.append(json.loads(line))

f = open("football_and_teams_final.json", "w", encoding="utf-8")
f.write(json.dumps(data))
f.close()

# f = open("data/football_and_teams_final(object).json", "w", encoding="utf-8")
# f.write("\n".join(str(v) for v in data))
# f.close()
#
# print(len(data))