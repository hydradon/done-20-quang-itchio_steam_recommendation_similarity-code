# Set up twitter API
import tweepy

twitter_consumer_key = "znjwTvSFCQ8KghPfPytaFLFMI"
twitter_consumer_secret = "TPfLye1l9pieYSYhGJuzowmmJP2gVXv9esxzzzDCxtEA0z5uoC"
twitter_access_token = "92231432-e7Xljzr86VgT5g7qVjhm7afLv98eTxO9hkT7Q5Wex"
twitter_access_token_secret = "NCL1O7E15dkKgfD3cLei6GbwFgWjh41jztqpwPAXZyJDD"

# auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
# auth.set_access_token(twitter_access_token, twitter_access_token_secret)

auth = tweepy.AppAuthHandler(twitter_consumer_key, twitter_consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, 
                       wait_on_rate_limit_notify=True)

# Retrieve developers Twitter handles
import pandas as pd


# DataFrame storing a game mapping to each of its developer's teams
df_game_dev_pair = pd.read_csv("../dataset/df_game_dev_pair.csv")

# DataFrame storing profile pages of each developer team
df_dev_contacts = pd.read_csv("../dataset/itch_dev_contacts_cleaned.csv", delimiter="\t")

df_dev_contacts.dropna(subset=['main_twitter_link'], inplace=True) # Drop developer teams who don't have Twitter
df_dev_contacts["main_twitter_link"] = df_dev_contacts["main_twitter_link"].map(lambda x: x.split("||")) # Split to individual. Eg: "user_url1||user_url2||user_url3" -> ["user_url1", "user_url2", "user_url3"]
df_dev_contacts["team_size"] = df_dev_contacts["main_twitter_link"].map(lambda x: len(x))

# Merging a game with its developer teams' profile pages
df_game_devteam_pair = df_dev_contacts.merge(df_game_dev_pair, left_on="game_developers_url", right_on="game_developers_url", how="left")
# Only keep these columns
df_game_devteam_pair = df_game_devteam_pair[["game_url", "game_developers_url", "num_devs", "main_twitter_link", "team_size"]]

df_game_devteam_pair = df_game_devteam_pair.explode("main_twitter_link")

dev_twitter_to_game_list = {} # A dictionary storing mappings of each developer to all of the games developed by the developer's team
for i, row in df_game_devteam_pair.iterrows():
    dev_twitter_to_game_list.setdefault(row["main_twitter_link"], []).append(row["game_url"])



# For testing - sample developers who make multiple games
sample_dev_twitters = [key for key in dev_twitter_to_game_list.keys() if len(dev_twitter_to_game_list[key]) > 1][:5]

non_existent_users = []

for twitter_link in sample_dev_twitters:
    # extract Twitter user first
    username = twitter_link.split("/")[-1]
    # print("Games made by user " + username)
    # print(dev_twitter_to_game_list[twitter_link])
    try :
        # user = api.get_user(username)
        # get_user_details(username)
        print(compose_message(twitter_link))
        # user_id = user.id_str
        # api.send_direct_message(user_id, compose_message())
    except tweepy.TweepError as err:
        print("Error is: ", err)
        non_existent_users.append({'user' : username, 
                                'error': err.args[0][0]['message']
                                })

def get_user_details(username):
    user = api.get_user(username)
    print("User details:")
    print(user.name)
    print(user.description)
    print(user.location)


def compose_message(twitter_link) -> str:
    username = twitter_link.split("/")[-1]
    game_list = dev_twitter_to_game_list[twitter_link]

    msg = "Dear @" + username + ". Your games are: " + ", ".join(game_list)

    return msg