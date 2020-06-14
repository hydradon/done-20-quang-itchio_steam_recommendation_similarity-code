import pandas as pd

df_ratings = pd.read_csv("../dataset/ratings_result.csv")

df_temp = pd.read_csv("../dataset/df_merge_temp.csv")
num_itch = 2830

df_itch = df_temp[:num_itch]
df_steam = df_temp[num_itch:]

df_ratings_match = df_ratings[df_ratings["is_upvote"] == 1]
df_ratings_nomatch = df_ratings[df_ratings["is_upvote"] == 0]