import pandas as pd
import numpy as np
import csv
import os
header = ["genre", "count"]

df2 = pd.read_csv('../dataset/df_itch_cleaned.csv')

df2['game_genres'] = df2['game_genres'].replace(np.nan, '', regex=True)
genre_count = {}
                   
for i, row in df2.iterrows():
    genres = row['game_genres'].lower().split("||")
    for item in genres:

        if item not in genre_count:
            genre_count[item] = 0
        genre_count[item] += 1

output = "../dataset/itch_genre_count.csv"
if os.path.exists(output):
    os.remove(output)

with open(output, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    for key in genre_count:
        writer.writerow({'genre': key, 'count': genre_count[key]})

f.close()



df_steam = pd.read_csv('../dataset/top_500_steam_sellers_details_raw_no_DLC.csv')
df_steam['game_genres'] = df_steam['game_genres'].replace(np.nan, '', regex=True)
genre_count = {}
                   
for i, row in df_steam.iterrows():
    genres = row['game_genres'].lower().split("||")
    for item in genres:
        if item not in genre_count:
            genre_count[item] = 0
        genre_count[item] += 1

output = "../dataset/steam_genre_count.csv"
if os.path.exists(output):
    os.remove(output)
with open(output, 'w', encoding='utf-8-sig', newline='') as f2:
    writer = csv.DictWriter(f2, fieldnames=header)
    writer.writeheader()
    for key in genre_count:
        writer.writerow({'genre': key, 'count': genre_count[key]})

f2.close()
