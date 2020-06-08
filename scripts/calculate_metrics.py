import pandas as pd
import numpy as np
import os


df_ratings = pd.read_csv("../dataset/ratings_result.csv")
df_similarity_scores = pd.read_csv("../dataset/df_5_recommendation_all.csv")

# NOTE P@K
def precision_at_k(vote_array) -> []:
    res = []
    sum = 0
    for i, v in enumerate(vote_array):
        sum += v
        res.append(sum/float(i+1))

    return res

# NOTE AP@K should be normalized by N, not the total number of relevant doc (unknown)
# Ref: https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-39940-9_487#:~:text=In%20Average%20Precision%20it%20is,%2C%20i.e.%2C%20NF%20%3D%20R.&text=For%20example%2C%20if%20one%20knows,an%20AP%4020%20of%200.2.
def ave_precision_at_k(vote_array, precision_array) -> []:
    ap_sum = 0
    ap_res = []
    for i, p, v in zip(range(len(precision_array)), precision_array, vote_array):
        ap_sum += (p * v)
        ap_res.append(ap_sum/float(i+1))

    return ap_res


# this calculate precision at k for each itch_game, df_input is all rec voting of 1 itch game
def calculate_precision_at_k(df_input) -> {}:
    df_input.sort_values(by=['sim_scores', 'u_id', 'timestamp', 'is_upvote'], 
                        ascending=[False, True, True, False], inplace=True)

    all_voters = df_input["u_id"].drop_duplicates().tolist()

    array_of_precision_at_k_aray = [] # size = number of voter, each element is an array of votes for 5 recs
    array_of_ave_precision_at_k_aray = []

    for voter in all_voters: # processing for each voter
        voter_votes = df_input[df_input["u_id"] == voter]

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


# Get all unique itch game with survey response
all_itch_games = df_ratings["itch_game_url"].drop_duplicates().tolist()

all_precision = {}
for itch_game in all_itch_games:
    # Extract all voting for a game
    df_voting = df_ratings[df_ratings["itch_game_url"] == itch_game]

    # TODO resolve recommendation where 2 sim scores are equal
    all_precision[itch_game] = calculate_precision_at_k(df_voting)

df_result = pd.DataFrame.from_dict(all_precision, orient='index').rename_axis('itch_game_url').reset_index()



# Save temporary df_merge to file
output = "../dataset/df_precision.csv"
if os.path.exists(output):
    os.remove(output)
df_result.to_csv(output, encoding='utf-8-sig', index=False)


