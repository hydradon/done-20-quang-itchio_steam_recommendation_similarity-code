import pandas as pd
import numpy as np
import csv
import os
header = ["tag", "count"]

df2 = pd.read_csv('../dataset/df_itch_cleaned.csv')

df2['game_tags'] = df2['game_tags'].replace(np.nan, '', regex=True)
tags_count = {}
                   
for i, row in df2.iterrows():
    tags = row['game_tags'].lower().split("||")
    for item in tags:

        if item not in tags_count:
            tags_count[item] = 0
        tags_count[item] += 1

output = "../dataset/itch_tag_count.csv"
if os.path.exists(output):
    os.remove(output)

with open(output, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    for key in tags_count:
        writer.writerow({'tag': key, 'count': tags_count[key]})

f.close()



df_steam = pd.read_csv('../dataset/top_500_steam_sellers_details_raw_no_DLC.csv')
df_steam['game_tags'] = df_steam['game_tags'].replace(np.nan, '', regex=True)
tag_count = {}
                   
for i, row in df_steam.iterrows():
    tags = row['game_tags'].lower().split("||")
    for item in tags:
        if item not in tag_count:
            tag_count[item] = 0
        tag_count[item] += 1

output = "../dataset/steam_tag_count.csv"
if os.path.exists(output):
    os.remove(output)
with open(output, 'w', encoding='utf-8-sig', newline='') as f2:
    writer = csv.DictWriter(f2, fieldnames=header)
    writer.writeheader()
    for key in tag_count:
        writer.writerow({'tag': key, 'count': tag_count[key]})

f2.close()
