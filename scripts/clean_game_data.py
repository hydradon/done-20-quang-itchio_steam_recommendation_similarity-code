import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem import SnowballStemmer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from rake_nltk import Metric, Rake
import re
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

stemmer = SnowballStemmer("english", ignore_stopwords=True)

# Read itch and steam game data
df_itch = pd.read_csv('../dataset/game_details_raw.csv')
df_steam = pd.read_csv('../dataset/top_steam_game_details_raw.csv')

df_itch.dropna(subset=['game_developers'], inplace=True) # Remove games without developers
df_itch = df_itch[df_itch["game_desc_len"] > 150] # Remove games with < 150 characters in description length (1st quartile)

df_small = df_itch.copy()[:50] # For testing
df_small = df_small.reset_index()  #NOTE only when using df_small

# Columns to retained
column_used = ["game_desc", "game_genres", "game_tags", "game_name", "game_url"]
df_small = df_small[column_used]
df_steam = df_steam[column_used]

# Extract keywords from description
def extract_keywords_from_description(df):
    df['keywords'] = ""
    df['keywords'] = df['keywords'].astype(object)
    for index, row in df.iterrows():
        # description = re.sub(r'http\S+', '', description) # Remove HTTP link
        description = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", row['game_desc'])

        # instantiating Rake, by default it uses english stopwords from NLTK
        # and discards all puntuation characters as well
        r = Rake(stopwords=stop_words, min_length=2)

        # extracting the words by passing the text
        r.extract_keywords_from_text(description)

        # getting the dictionary whith key words as keys and their scores as values
        key_words_dict_scores = r.get_word_degrees()
        
        # assigning the key words to the new column for the corresponding movie
        df.at[index, 'keywords'] = [stemmer.stem(keyword)                                 # Perform stemming on keywords
                                        for keyword in list(key_words_dict_scores.keys()) 
                                        if re.match(r'[^\W\d]*$', keyword)]               # Remove nonalphabetical characters

extract_keywords_from_description(df_small)
extract_keywords_from_description(df_steam) 


# process genres and tags columns
def clean_data(x):
    return [str.lower(i.replace(" ", "")) for i in x]

def clean_columns(column_list, df):
    for col in column_list:
        df[col].replace(np.nan, "", inplace=True)
        df[col] = df[col].map(lambda x: x.split("||"))
        df[col] = df[col].apply(clean_data)

column_list = ["game_genres", "game_tags"]
clean_columns(column_list, df_small)
clean_columns(column_list, df_steam)


# Create a soup column of genres, tags, and keywords
def create_soup(x):
    return ' '.join(x['game_genres']) + \
            ' ' + ' '.join(x['game_tags']) + \
            ' ' + ' '.join(x['keywords'])

df_small['soup'] = df_small.apply(create_soup, axis=1)
df_steam['soup'] = df_steam.apply(create_soup, axis=1)


# Reverse index, ie. get game index by name
indices = pd.Series(df_small.index, index=df_small['game_name']).drop_duplicates()

# Create document vectors
count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
# count = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')

count_matrix_itch = count.fit_transform(df_small['soup'])
count_matrix_steam = count.fit_transform(df_steam['soup'])

# Calculate cosine similarity
# cosine_sim = linear_kernel(count_matrix, count_matrix)              # Used when TfidfVectorizer is used
cosine_sim = cosine_similarity(count_matrix_itch, count_matrix_steam) # Used when CountVectorizer is used


# Recommend game based on a game_name
def get_recommendations(game_name, cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[game_name]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[0:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df_small['game_name'].iloc[movie_indices]

def get_recommendations2(game_name, cosine_sim):
    idx = indices[game_name]

    # Get a list of tuples (sim_score, name, url) 
    similar_indices = cosine_sim[idx].argsort()[:-12:-1]
    sim_scores2 = [(cosine_sim[idx][i], df_small['game_name'][i], df_small["game_url"][i]) for i in similar_indices]

    return sim_scores2