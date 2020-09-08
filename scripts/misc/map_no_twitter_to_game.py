# Retrieve developers Twitter handles
import pandas as pd


# DataFrame storing a game mapping to each of its developer's teams
df_game_dev_pair = pd.read_csv("../dataset/df_game_dev_pair.csv")

# DataFrame storing profile pages of each developer team
df_dev_contacts = pd.read_csv("../dataset/itch_dev_contacts_cleaned.csv", delimiter="\t")

df_dev_contacts = df_dev_contacts[df_dev_contacts["main_twitter_link"].isna()]  # Drop developer teams who have Twitter
df_dev_contacts = df_dev_contacts[df_dev_contacts["twitter_links"].isna()]

df_test = df_dev_contacts.dropna(subset=["discord_links", "emails", "facebook_links", "other_links"], how="all") # Drop those who dont have anything




# Merging a game with its developer teams' profile pages
df_game_devteam_pair = df_test.merge(df_game_dev_pair, left_on="game_developers_url", right_on="game_developers_url", how="left")

# Drop rows where there is no game name
df_game_devteam_pair.dropna(subset=["game_name"], inplace=True)

# Drop Twitter columns
df_game_devteam_pair.drop(["main_twitter_link", "twitter_links"], axis=1, inplace=True)



import random
import string
def get_random_alphaNumeric_string(stringLength=32):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


# Current UID set
uid = pd.read_csv("../dataset/curr_u.csv")
uid_set = set(uid["uid"].tolist())

# Append UID
extra_limit = len(df_game_devteam_pair["game_developers_url"].drop_duplicates().tolist())
extra_set = set()

dev_itch_link_uid = {}


while len(extra_set) < extra_limit:
    new_id = get_random_alphaNumeric_string(32)
    if new_id not in uid_set and new_id not in extra_set:
        extra_set.add(new_id)
        uid_set.add(new_id)


for i, row in df_game_devteam_pair.iterrows():
    current_dev_itch_url = row["game_developers_url"]

    if current_dev_itch_url not in dev_itch_link_uid:
        dev_itch_link_uid[current_dev_itch_url] = extra_set.pop()

    df_game_devteam_pair.loc[i, 'uid'] = dev_itch_link_uid[current_dev_itch_url]


# Save to file
output = "../dataset/df_other_contact_to_game_nam_url.csv"
import os
if os.path.exists(output):
    os.remove(output)
df_game_devteam_pair.to_csv(output, encoding='utf-8-sig', index=False)




import pymysql
def save_to_database(df_results, table):
    
    # Connect to the database
    connection = pymysql.connect(host='localhost', db='gamerecs',
                                 user='root', password='evermore9')
    # create cursor
    cursor=connection.cursor()
    cols = "`,`".join([str(i) for i in df_results.columns.tolist()])

    for i,row in df_results.iterrows():
        sql = "INSERT INTO `" + table + "` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))

        # the connection is not autocommitted by default, so we must commit to save our changes
        connection.commit()

df_game_devteam_pair_red = df_game_devteam_pair[['game_developers_url', 'game_name', 'game_url', "uid"]]  
df_game_devteam_pair_red.rename(columns={"game_developers_url" : "dev_itch_link"}, inplace=True)
save_to_database(df_game_devteam_pair_red, "game_twitter_devs")
