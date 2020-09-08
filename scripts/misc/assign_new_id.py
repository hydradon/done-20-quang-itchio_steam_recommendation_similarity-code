#%%
import random
import string

def get_random_alphaNumeric_string(stringLength=32):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


import pandas as pd

twitter_uid = pd.read_csv("../dataset/df_twitter_uid.csv")
game_twitter_devs = pd.read_csv("../dataset/df_each_twitter_to_game_name_url_2.csv")


limit = len(twitter_uid)
total = set()

while len(total) < limit:
    total.add(get_random_alphaNumeric_string(32))

for i, row in twitter_uid.iterrows():
    twitter_uid.loc[i, 'uid'] = total.pop()

import os
output = "../dataset/df_twitter_uid.csv"
if os.path.exists(output):
    os.remove(output)
twitter_uid.to_csv(output, encoding='utf-8-sig', index=False)

twitter_uid_dict = {}
for i, row in twitter_uid.iterrows():
    twitter_uid_dict[row["main_twitter_link"]] = row['uid']

for i, row in game_twitter_devs.iterrows():
    game_twitter_devs.loc[i, 'uid'] = twitter_uid_dict[row["main_twitter_link"]]

output = "../dataset/df_each_twitter_to_game_name_url_2.csv"
if os.path.exists(output):
    os.remove(output)
game_twitter_devs.to_csv(output, encoding='utf-8-sig', index=False)


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