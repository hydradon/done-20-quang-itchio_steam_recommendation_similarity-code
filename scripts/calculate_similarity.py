import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from nltk.stem import SnowballStemmer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from rake_nltk import Metric, Rake
import re
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

stemmer = SnowballStemmer("english", ignore_stopwords=True)

# Read itch and steam game data
df_itch = pd.read_csv('../dataset/game_details_raw.csv')
# df_steam = pd.read_csv('../dataset/top_500_steam_sellers_details_raw.csv')
df_steam = pd.read_csv('../dataset/top_500_steam_sellers_details_raw_no_DLC.csv')

# Data filtering
df_itch.dropna(subset=['game_developers'], inplace=True)  # Remove games without developers
df_itch = df_itch[df_itch["game_desc_len"] > 150]         # Remove games with <= 150 characters in description length (1st quartile)
df_itch = df_itch[df_itch["game_language"] == "English"]  # Only keep English games
df_itch.fillna(value={"game_no_ratings" : 0}, inplace=True)
df_itch = df_itch[df_itch["game_no_ratings"] > 4]         # Keep games with at least 5 ratings, for ease of computation
                                                          # and for survey

df_itch = df_itch.reset_index()

# df_itch = df_itch.copy()[:50] # For testing
df_itch_num_ratings = df_itch[["game_name", "game_url", "game_no_ratings"]]     # Keep num ratings for itch
df_steam_short_desc = df_steam[["game_name", "game_url", "game_desc_snippet"]]  # Keep Steam game desc for display on page


# Columns to retained
column_used = ["game_desc", "game_genres", "game_tags", "game_name", "game_url"]
df_itch = df_itch[column_used]
df_steam = df_steam[column_used]
df_steam["game_genres"] = df_steam["game_genres"].str \
                            .lower().replace(regex={r'massively multiplayer' :'multiplayer', 
                                                    r'rpg': 'roleplaying',
                                                    r'crpg': 'roleplaying'})
# Concatenate itch and steam df
df_merge = pd.concat([df_itch, df_steam], ignore_index=True)

# Extract keywords from description
def extract_keywords_from_description(df):
    df['keywords'] = ""
    df['keywords'] = df['keywords'].astype(object)
    for index, row in df.iterrows():
        # description = re.sub(r'http\S+', '', description) # Remove HTTP link
        description = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", row['game_desc'])

        # instantiating Rake, by default it uses english stopwords from NLTK
        # and discards all puntuation characters as well
        r = Rake(stopwords=stop_words, min_length=3)

        # extracting the words by passing the text
        r.extract_keywords_from_text(description)

        # getting the dictionary with key words as keys and their scores as values
        key_words_dict_scores = r.get_word_degrees()
        
        # assigning the key words to the new column for the corresponding movie
        df.at[index, 'keywords'] = [stemmer.stem(keyword)                                 # Perform stemming on keywords
                                        for keyword in list(key_words_dict_scores.keys()) 
                                        if re.match(r'[^\W\d]*$', keyword)                # Remove nonalphabetical characters
                                        and not re.match(r'^_+$', keyword)]               # Remove words with only "_"

# extract_keywords_from_description(df_itch)  # for debugging
# extract_keywords_from_description(df_steam)  # for debugging
extract_keywords_from_description(df_merge)

# process genres and tags columns
def clean_data(x):
    return [str.lower(i.replace(" ", "")) for i in x]

def clean_columns(column_list, df):
    for col in column_list:
        df[col].replace(np.nan, "", inplace=True)
        df[col] = df[col].map(lambda x: x.split("||"))
        df[col] = df[col].apply(clean_data)

column_list = ["game_genres", "game_tags"]
# clean_columns(column_list, df_itch)
# clean_columns(column_list, df_steam)
clean_columns(column_list, df_merge)

# Save temporary df_merge to file
output = "../dataset/df_merge_temp_temp.csv"
if os.path.exists(output):
    os.remove(output)
df_merge.to_csv(output, encoding='utf-8-sig', index=False)

# Create a soup column of genres, tags, and keywords
def create_soup(x):
    return ' '.join(x['game_genres']) + \
            ' ' + ' '.join(x['game_tags']) + \
            ' ' + ' '.join(x['keywords'])


df_merge['soup'] = df_merge.apply(create_soup, axis=1)
df_merge['soup_tags'] = df_merge["game_tags"].map(lambda x: ' '.join(x))
df_merge['soup_genres'] = df_merge["game_genres"].map(lambda x: ' '.join(x))
df_merge['soup_desc'] = df_merge["keywords"].map(lambda x: ' '.join(x))

# Reverse index, ie. get game index by name
indices = pd.Series(df_merge.index, index=df_merge['game_name']).drop_duplicates()
# Reverse index, wrt game_url
indices_game_url = pd.Series(df_merge.index, index=df_merge['game_url']).drop_duplicates()


# Create document vectors
count_mix = CountVectorizer(analyzer='word', ngram_range=(1, 1), 
                        min_df=0, max_df=0.50, 
                        stop_words='english')                      
# count_mix = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), 
#                         min_df=0, max_df=0.50, 
#                         stop_words='english')
count_matrix_mix = count_mix.fit_transform(df_merge['soup'])


# Tag similarity only
count_tags = CountVectorizer(analyzer='word', ngram_range=(1, 1))
count_matrix_tags = count_tags.fit_transform(df_merge['soup_tags'])

# Genre similarity only
count_genres = CountVectorizer(analyzer='word', ngram_range=(1, 1))
count_matrix_genres = count_genres.fit_transform(df_merge['soup_genres'])

# Desc similarity only
count_desc = CountVectorizer(analyzer='word', ngram_range=(1, 1), stop_words='english')
count_matrix_desc = count_desc.fit_transform(df_merge['soup_desc'])

# Calculate cosine similarity
# cosine_sim_tfidf = linear_kernel(count_matrix, count_matrix)           # Used when TfidfVectorizer is used
cosine_sim_mix = cosine_similarity(count_matrix_mix, count_matrix_mix)   # Used when CountVectorizer is used
cosine_sim_tags = cosine_similarity(count_matrix_tags, count_matrix_tags)
cosine_sim_genres = cosine_similarity(count_matrix_genres, count_matrix_genres)
cosine_sim_desc = cosine_similarity(count_matrix_desc, count_matrix_desc)

# Extract individual sub recommendation unit scores NOTE: don't do this temporarily
sim_scores_tags = cosine_sim_tags[0:len(df_itch), len(df_itch):]
sim_scores_genres = cosine_sim_genres[0:len(df_itch), len(df_itch):]
sim_scores_desc = cosine_sim_desc[0:len(df_itch), len(df_itch):]


# Combine final recommendation weight = matrix [tag_weight, genre_weight, desc_weight]
def combine_recommendation(weight, sim_scores_tags, sim_scores_genres, sim_scores_desc):
    return weight[0] * sim_scores_tags + weight[1] * sim_scores_genres + weight[2] * sim_scores_desc


# sim_scores_combined_tags_inclined = combine_recommendation([0.5, 0.25, 0.25], sim_scores_tags, sim_scores_genres, sim_scores_desc)
# sim_scores_combined_genres_inclined = combine_recommendation([0.25, 0.5, 0.25], sim_scores_tags, sim_scores_genres, sim_scores_desc)
# sim_scores_combined_desc_inclined = combine_recommendation([0.25, 0.25, 0.5], sim_scores_tags, sim_scores_genres, sim_scores_desc)

sim_scores_combined_tags_inclined = combine_recommendation([0.5, 0.25, 0.25], cosine_sim_tags, cosine_sim_genres, cosine_sim_desc)
sim_scores_combined_genres_inclined = combine_recommendation([0.25, 0.5, 0.25], cosine_sim_tags, cosine_sim_genres, cosine_sim_desc)
sim_scores_combined_desc_inclined = combine_recommendation([0.25, 0.25, 0.5], cosine_sim_tags, cosine_sim_genres, cosine_sim_desc)

# def get_recommendations2(game_name, cosine_sim, top_n):
#     idx = indices[game_name]

#     # Get a list of tuples (sim_score, name, url) 
#     similar_indices = cosine_sim[idx].argsort()[:-top_n-1:-1]
#     sim_scores2 = [(cosine_sim[idx][i], df_itch['game_name'][i], df_itch["game_url"][i]) for i in similar_indices]

#     return sim_scores2

# Recommend game based on a game_url
def get_recommendations_on_url(game_url, cosine_sim, top_n):
    # Get the index of the Itch game that matches the title
    it_game_idx = indices_game_url[game_url]

    # Get the pairwise similarity scores of all games with that Itch game
    sim_scores = list(enumerate(cosine_sim[it_game_idx]))

    # Obtain only the similarity to Steam games
    sim_scores = sim_scores[len(df_itch):]

    # Sort the Steam games based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the top n most similar Steam games
    sim_scores = sim_scores[0:top_n]

    # Get the Steam game indices
    st_game_indices = [i[0] for i in sim_scores]

    results = pd.DataFrame({"itch_game"        : df_merge['game_name'].iloc[it_game_idx],
                            "itch_game_url"    : game_url,
                            "steam_game"       : [df_merge['game_name'].iloc[st_game_idx] for st_game_idx in st_game_indices],
                            "steam_game_index" : st_game_indices,
                            "steam_game_url"   : [df_merge['game_url'].iloc[st_game_idx] for st_game_idx in st_game_indices],
                            "sim_scores"       : [x[1] for x in sim_scores]
                           })
    return results


def get_recommendation_all_itch_games(cosine_sim, top_n):
    all_itch_game_url = df_itch["game_url"].tolist()

    df_result = pd.DataFrame()

    for it_game_url in all_itch_game_url:
        # print(itch_game)
        batch = get_recommendations_on_url(it_game_url, cosine_sim, top_n)
        # Conccatenate itch and steam df
        df_result = pd.concat([df_result, batch], ignore_index=True)

    return df_result

# Get all top 10 Steam recommendations for each Itch games
top_n = 5
df_result = get_recommendation_all_itch_games(cosine_sim_mix, top_n)
df_result_tags = get_recommendation_all_itch_games(sim_scores_combined_tags_inclined, top_n)
df_result_genres = get_recommendation_all_itch_games(sim_scores_combined_genres_inclined, top_n)
df_result_desc = get_recommendation_all_itch_games(sim_scores_combined_desc_inclined, top_n)


def process_final_df(df_result, component):
    # Attach Steam game short desc
    df_final = df_result.merge(df_steam_short_desc, left_on="steam_game_url", right_on="game_url")
    df_final.drop(["game_name", "game_url"], inplace=True, axis=1) # drop redundant Steam game_name and game_url

    # Merge with num ratings
    df_final = df_final.merge(df_itch_num_ratings, left_on="itch_game_url", right_on="game_url")
    df_final.drop(["game_name", "game_url"], inplace=True, axis=1) # drop redundant itch game_name and game_url

    df_final["sim_scores"] = df_final["sim_scores"].map('{:,.9f}'.format) # Format the contribution to 9 decimal places
    df_final["row_id"] = df_final.index
    df_final["itch_game_url"] = "https://" + df_final["itch_game_url"]
    df_final["game_desc_snippet"] = df_final["game_desc_snippet"].fillna("")

    df_final.sort_values(by=['itch_game', 'sim_scores', 'row_id'], ascending=[True, False, True], inplace=True)

    # Save temporary df_merge to file
    output = "../dataset/df_" + str(top_n) + "_recommendation_all_9dp_" + component + ".csv"
    if os.path.exists(output):
        os.remove(output)
    df_final.to_csv(output, encoding='utf-8-sig', index=False)

process_final_df(df_result, "mix")
process_final_df(df_result_tags, "tag")
process_final_df(df_result_genres, "genre")
process_final_df(df_result_desc, "desc")
