# Dataset description

## Game metadata

[top_500_steam_sellers_details_raw_no_DLC.csv](./top_500_steam_sellers_details_raw_no_DLC.csv): 326 top-selling games and their description.

[games_raw.csv](./games_raw.csv): all itch.io games.

[game_details_raw.csv](./game_details_raw.csv): all itch.io games with their metadata.

[df_itch_cleaned.csv](./df_itch_cleaned.csv): 2,830 itch.io games used for analysis.


## Developer details

[df_game_dev_pair.csv](./dev_contact/df_game_dev_pair.csv): the developer's itch.io profile page for each itch.io game.

[itch_dev_contacts_cleaned.csv](./dev_contact/itch_dev_contacts_cleaned.csv): all developers' public contact details for 2,830 itch.io games.

[df_each_twitter_to_game_name_url_2.csv](./dev_contact/df_each_twitter_to_game_name_url_2.csv): used to generated message to send to each developer for evaluation (for those who have Twitter).

[df_other_contact_to_game_nam_url.csv](./dev_contact/df_other_contact_to_game_nam_url): used to generated message to send to each developer for evaluation (for those who do not have Twitter).

[df_devs_no_twitter.csv](./dev_contact/df_devs_no_twitter.csv): developers' public contact details for 2,830 itch.io games for those whose Twitter is not contactable.

[game_twitter_devs.tbl.csv](./dev_contact/game_twitter_devs.tbl.csv): used for checking if a developer can submit an evaluation for a game. **NOTE: This should be used when rebuilding database for the webpage.**


## Itch and matched Steam games

[df_5_recommendation_all_9dp_desc.csv](./df_5_recommendation_all_9dp_desc.csv): top 5 matched Steam games where description similarity is heavily weighted.

[df_5_recommendation_all_9dp_genre.csv](./df_5_recommendation_all_9dp_genre.csv): top 5 matched Steam games where genre similarity is heavily weighted.

[df_5_recommendation_all_9dp_tag.csv](./df_5_recommendation_all_9dp_tag.csv): top 5 matched Steam games where tag similarity is heavily weighted.

[df_5_recommendation_all_9dp_mix.csv](./df_5_recommendation_all_9dp_mix.csv): top 5 matched Steam games where all description, tag, and genre are mixed in a bag of words and similarity score is calculated.

[df_5_recommendation_all_9dp_combined.csv](./df_5_recommendation_all_9dp_combined.csv): combined list of all top 5 matched Steam games from the above datasets. **NOTE: This should be used when rebuilding database for the webpage.**


## Results

[positive_negative_overall_feedback.xlsx](./results/positive_negative_overall_feedback.xlsx): the overall feedback responses that have been categorized as positive/negative/neutral.

[Reasons_for_Bad_recommendation_matches_Random_sample.xlsx](./results/Reasons_for_Bad_recommendation_matches_Random_sample.xlsx): a random sample of reasons for downvoted recommendations with open-coding results.

