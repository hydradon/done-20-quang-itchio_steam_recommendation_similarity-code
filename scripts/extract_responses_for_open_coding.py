import pandas as pd

df_ratings = pd.read_csv("../dataset/ratings.csv")
 
# Drop some duplicates
df_ratings_nodup = df_ratings.sort_values('timestamp').drop_duplicates(subset=['itch_game_url', 'steam_game_url', 'u_id'], keep='last')
df_ratings_nodup_feedback = df_ratings_nodup[["itch_game_url", "steam_game_url", "feedback", "is_upvote"]]
df_ratings_nodup_feedback.dropna(subset=["feedback"], inplace=True)


df_ratings_match = df_ratings_nodup_feedback[df_ratings_nodup_feedback["is_upvote"] == 1]
df_ratings_nomatch = df_ratings_nodup_feedback[df_ratings_nodup_feedback["is_upvote"] == 0]

df_ratings_match.drop(columns=["is_upvote", "overall_feedback"], inplace=True)
df_ratings_nomatch.drop(columns=["is_upvote", "overall_feedback"], inplace=True)

import os
# Save to file
output = "../dataset/df_reasons_no_nmatch.csv"
if os.path.exists(output):
    os.remove(output)
df_ratings_nomatch.to_csv(output, encoding='utf-8-sig', index=False)

output = "../dataset/df_reasons_match.csv"
if os.path.exists(output):
    os.remove(output)
df_ratings_match.to_csv(output, encoding='utf-8-sig', index=False)


# Extract overall feedback
df_ratings_nodup_overall_feedback = df_ratings_nodup[["itch_game_url", "steam_game_url", "overall_feedback", "is_upvote"]]
df_ratings_nodup_overall_feedback.dropna(subset=["overall_feedback"], inplace=True)

# Since overall feedback is the same for an Itch game, drop the duplicates overall_feedback
df_ratings_nodup_overall_feedback.drop_duplicates(subset=['overall_feedback'], inplace=True)
df_ratings_nodup_overall_feedback.drop(columns=["steam_game_url", "is_upvote"], inplace=True)

output = "../dataset/df_overall_feedback.csv"
if os.path.exists(output):
    os.remove(output)
df_ratings_nodup_overall_feedback.to_csv(output, encoding='utf-8-sig', index=False)
