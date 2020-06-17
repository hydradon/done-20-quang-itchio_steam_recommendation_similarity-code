import pandas as pd

df_recs_mix = pd.read_csv('../dataset/df_5_recommendation_all_9dp_mix.csv')
df_recs_tag = pd.read_csv('../dataset/df_5_recommendation_all_9dp_tag.csv')
df_recs_genre = pd.read_csv('../dataset/df_5_recommendation_all_9dp_genre.csv')
df_recs_desc = pd.read_csv('../dataset/df_5_recommendation_all_9dp_desc.csv')


df_result = pd.concat([df_recs_mix, df_recs_tag, df_recs_genre, df_recs_desc], ignore_index=True)

df_test = df_result.drop_duplicates(subset=["itch_game_url", "steam_game_url"], ignore_index=True)
df_test.sort_values(by=["itch_game_url", "steam_game_url"], inplace=True)

# Randomize order
from sklearn.utils import shuffle
df_test = shuffle(df_test)

import os
output = "../dataset/df_5_recommendation_all_9dp_combined.csv"
if os.path.exists(output):
    os.remove(output)
df_test.to_csv(output, encoding='utf-8-sig', index=False)


# Count
num_recs = df_test.groupby(["itch_game_url"]).size().reset_index(name='counts')
output = "../dataset/num_recs.csv"
if os.path.exists(output):
    os.remove(output)
num_recs.to_csv(output, encoding='utf-8-sig', index=False)







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

save_to_database(df_test, "toprecs")
