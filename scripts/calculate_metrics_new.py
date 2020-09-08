import pandas as pd
import numpy as np
import os
import json

df_recs_mix = pd.read_csv('../dataset/df_5_recommendation_all_9dp_mix.csv')
df_recs_tag = pd.read_csv('../dataset/df_5_recommendation_all_9dp_tag.csv')
df_recs_genre = pd.read_csv('../dataset/df_5_recommendation_all_9dp_genre.csv')
df_recs_desc = pd.read_csv('../dataset/df_5_recommendation_all_9dp_desc.csv')
# df_recs_combined = pd.read_csv('../dataset/df_5_recommendation_all_9dp_combined.csv')
df_ratings = pd.read_csv('../dataset/ratings.csv')
df_ratings.drop(["sim_scores", "row_id"], axis=1, inplace=True)

df_itch = pd.read_csv("../dataset/df_itch_cleaned.csv")
df_itch["itch_game_url"] = "https://" + df_itch["game_url"]
df_itch.fillna(value={"game_genres" : "", "game_tags" : ""}, inplace=True)

# NOTE P@K
def precision_at_k(vote_array) -> []:
    res = []
    sum = 0
    for i, v in enumerate(vote_array):
        sum += v
        res.append(sum/float(i+1))

    return res

# NOTE AP@K should be normalized by K, not the total number of relevant doc (unknown)
# Ref: https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-39940-9_487#:~:text=In%20Average%20Precision%20it%20is,%2C%20i.e.%2C%20NF%20%3D%20R.&text=For%20example%2C%20if%20one%20knows,an%20AP%4020%20of%200.2.
def ave_precision_at_k(vote_array, precision_array) -> []:
    ap_sum = 0
    ap_res = []
    for i, p, v in zip(range(len(precision_array)), precision_array, vote_array):
        ap_sum += (p * float(v))
        ap_res.append(ap_sum/float(i+1))

    return ap_res

# this calculate precision at k for each itch_game, df_input is all rec voting of 1 itch game
def calculate_precision_at_k(df_input) -> {}:
    
    all_voters = df_input["u_id"].drop_duplicates().tolist()

    array_of_precision_at_k_aray = [] # size = number of voter, each element is an array of votes for 5 recs
    array_of_ave_precision_at_k_aray = []

    for voter in all_voters: # processing for each voter
        voter_votes = df_input[df_input["u_id"] == voter]
        voter_votes.sort_values(by=['sim_scores', 'row_id', 'timestamp'], 
                                ascending=[False, True, True], inplace=True)

        # Only keep the latest vote based on timestamp for each rec vote
        voter_votes.drop_duplicates('steam_game_url', keep='last', inplace=True) # NOTE reset_index(drop=True) ?

        # If this voter did not vote for all 5 recommendation, don't include them
        if len(voter_votes) < 5:
            continue
        else:
            vote_array = voter_votes["is_upvote"].tolist()
            precision_at_k_array = precision_at_k(vote_array)

            array_of_precision_at_k_aray.append(precision_at_k_array)
            array_of_ave_precision_at_k_aray.append(ave_precision_at_k(vote_array, precision_at_k_array))

    # calculate mean of all voters of all recs for an itch game
    return {"precision@k"     : np.mean(array_of_precision_at_k_aray, axis=0).tolist(),
            "ave_precision@k" : np.mean(array_of_ave_precision_at_k_aray, axis=0).tolist()}

rated_itch_games = df_ratings["itch_game_url"].drop_duplicates().tolist()

all_precision = []
for itch_game in rated_itch_games:
    # Extract all voting for a game
    df_voting = df_ratings[df_ratings["itch_game_url"] == itch_game]

    result = {"itch_game_url": itch_game,
              "genres" : df_itch[df_itch["itch_game_url"] == itch_game]["game_genres"].astype(str).values[0],
              "tags"   : df_itch[df_itch["itch_game_url"] == itch_game]["game_tags"].astype(str).values[0],
            }

    # Calculate all precisions
    # Tag inclined
    df_tag_rec = df_recs_tag[df_recs_tag["itch_game_url"] == itch_game]
    df_voting_tag = df_voting[df_voting["steam_game_url"].isin(df_tag_rec["steam_game_url"])] # Extract correct voting pair for this algo 
    df_voting_tag = df_voting_tag.merge(df_tag_rec, left_on="steam_game_url", right_on="steam_game_url")
    precision = calculate_precision_at_k(df_voting_tag)
    result["tag_p1"] = precision["precision@k"][0]
    result["tag_p3"] = precision["precision@k"][2]
    result["tag_p5"] = precision["precision@k"][4]
    result["tag_ap1"] = precision["ave_precision@k"][0]
    result["tag_ap3"] = precision["ave_precision@k"][2]
    result["tag_ap5"] = precision["ave_precision@k"][4]
    # result["tag_weighted"] = calculate_precision_at_k(df_voting_tag)

    # Genre inclined
    df_genre_rec = df_recs_genre[df_recs_genre["itch_game_url"] == itch_game]
    df_voting_genre = df_voting[df_voting["steam_game_url"].isin(df_genre_rec["steam_game_url"])] # Extract correct voting pair for this algo 
    df_voting_genre = df_voting_genre.merge(df_genre_rec, left_on="steam_game_url", right_on="steam_game_url")
    precision = calculate_precision_at_k(df_voting_genre)
    result["genre_p1"] = precision["precision@k"][0]
    result["genre_p3"] = precision["precision@k"][2]
    result["genre_p5"] = precision["precision@k"][4]
    result["genre_ap1"] = precision["ave_precision@k"][0]
    result["genre_ap3"] = precision["ave_precision@k"][2]
    result["genre_ap5"] = precision["ave_precision@k"][4]
    # result["genre_weighted"] = calculate_precision_at_k(df_voting_genre)

    # Desc inclined
    df_desc_rec = df_recs_desc[df_recs_desc["itch_game_url"] == itch_game]
    df_voting_desc = df_voting[df_voting["steam_game_url"].isin(df_desc_rec["steam_game_url"])] # Extract correct voting pair for this algo 
    df_voting_desc = df_voting_desc.merge(df_desc_rec, left_on="steam_game_url", right_on="steam_game_url")
    precision = calculate_precision_at_k(df_voting_desc)
    result["desc_p1"] = precision["precision@k"][0]
    result["desc_p3"] = precision["precision@k"][2]
    result["desc_p5"] = precision["precision@k"][4]
    result["desc_ap1"] = precision["ave_precision@k"][0]
    result["desc_ap3"] = precision["ave_precision@k"][2]
    result["desc_ap5"] = precision["ave_precision@k"][4]
    # result["desc_weighted"] = calculate_precision_at_k(df_voting_desc)

    # Mix  
    df_mix_rec = df_recs_mix[df_recs_mix["itch_game_url"] == itch_game]
    df_voting_mix = df_voting[df_voting["steam_game_url"].isin(df_mix_rec["steam_game_url"])] # Extract correct voting pair for this algo 
    df_voting_mix = df_voting_mix.merge(df_mix_rec, left_on="steam_game_url", right_on="steam_game_url")
    # result["mix"] = calculate_precision_at_k(df_voting_mix)
    precision = calculate_precision_at_k(df_voting_mix)
    result["mix_p1"] = precision["precision@k"][0]
    result["mix_p3"] = precision["precision@k"][2]
    result["mix_p5"] = precision["precision@k"][4]
    result["mix_ap1"] = precision["ave_precision@k"][0]
    result["mix_ap3"] = precision["ave_precision@k"][2]
    result["mix_ap5"] = precision["ave_precision@k"][4]



    all_precision.append(result)


with open('result1.json', 'w') as fp:
    fp.write(json.dumps(all_precision, indent=4))