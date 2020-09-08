# Retrieve developers Twitter handles
import pandas as pd


# DataFrame storing a game mapping to each of its developer's teams
df_game_dev_pair = pd.read_csv("../dataset/df_game_dev_pair.csv")

# DataFrame storing profile pages of each developer team
df_dev_contacts = pd.read_csv("../dataset/itch_dev_contacts_cleaned.csv", delimiter="\t")

df_dev_contacts.dropna(subset=['main_twitter_link'], inplace=True) # Drop developer teams who don't have Twitter
df_dev_contacts["main_twitter_link"] = df_dev_contacts["main_twitter_link"].map(lambda x: x.split("||")) # Split to individual. Eg: "user_url1||user_url2||user_url3" -> ["user_url1", "user_url2", "user_url3"]
# df_dev_contacts["team_size"] = df_dev_contacts["main_twitter_link"].map(lambda x: len(x))

# Merging a game with its developer teams' profile pages
df_game_devteam_pair = df_dev_contacts.merge(df_game_dev_pair, left_on="game_developers_url", right_on="game_developers_url", how="left")
# Only keep these columns
df_game_devteam_pair = df_game_devteam_pair[["game_name", "game_url", "game_developers_url", "num_devs", "main_twitter_link"]]

df_game_devteam_pair = df_game_devteam_pair.explode("main_twitter_link")

df_game_devteam_pair = df_game_devteam_pair[['main_twitter_link', 'game_name', 'game_url']]
df_game_devteam_pair.dropna(subset=['game_url'], inplace=True) # drop developer whose links to game are lost
# Append UID
df_uid = pd.read_csv("../dataset/df_twitter_uid.csv")
df_game_devteam_pair = df_game_devteam_pair.merge(df_uid, left_on="main_twitter_link", right_on="main_twitter_link", how="left")

# Save to file
output = "../dataset/df_each_twitter_to_game_name_url_2.csv"
import os
if os.path.exists(output):
    os.remove(output)
df_game_devteam_pair.to_csv(output, encoding='utf-8-sig', index=False)