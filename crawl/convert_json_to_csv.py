# import pandas as pd
#
# data = pd.read_json('football_and_teams.json', lines=True)
# print(data.text)

import pandas as pd

with open('football_and_teams.json', encoding='utf-8-sig') as f_input:
    df = pd.read_json(f_input, lines=True)

df.to_csv('football_and_teams.csv', encoding='utf-8', index=False)