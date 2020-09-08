import tweepy
import time
import pandas as pd
import logging
import sys
from datetime import datetime
import random

class TwitterMessenger:
    def __init__(self, start, end):
        logging.basicConfig(level=logging.INFO,
                            handlers=[logging.FileHandler('twitter_messenger_{:d}_{:d}_{:%Y-%m-%d %I-%M-%S}.log'.format(start, end, datetime.now()), 'w', 'utf-8-sig'),
                                      logging.StreamHandler(sys.stdout)],
                            format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    
        self.start = start
        self.end = end

        # Set up twitter API
        self.twitter_consumer_key = "znjwTvSFCQ8KghPfPytaFLFMI"
        self.twitter_consumer_secret = "TPfLye1l9pieYSYhGJuzowmmJP2gVXv9esxzzzDCxtEA0z5uoC"
        self.twitter_access_token = "92231432-v2O9M8dBZayyfQXtYZVFygO7lCiRhPoZlB4EolQZw"
        self.twitter_access_token_secret = "7tqhZfAfA8w2kr9cbQzbZ0nC1qZI2duflDvIk0Nyd7dYf"

        auth = tweepy.OAuthHandler(self.twitter_consumer_key, self.twitter_consumer_secret)
        auth.set_access_token(self.twitter_access_token, self.twitter_access_token_secret)

        # auth = tweepy.AppAuthHandler(self.twitter_consumer_key, self.twitter_consumer_secret) <- this can't be used to send message
        self.api = tweepy.API(auth, wait_on_rate_limit=True, 
                                    wait_on_rate_limit_notify=True,
                                    retry_count=3, 
                                    retry_delay=5)

        # Load df ->
        df_game_devteam_pair = pd.read_csv("../dataset/df_each_twitter_to_game_name_url_2.csv")
        df_game_devteam_pair.dropna(subset=['game_url'], inplace=True) # Drop developer whose links to games are lost
        self.dev_twitter_to_game_list = {} # A dictionary storing mappings of each developer to all of the games developed by the developer's team
        self.dev_twitter_uid = {} # A dictionary to map Dev twitter to UID
        for i, row in df_game_devteam_pair.iterrows():
            self.dev_twitter_to_game_list.setdefault(row["main_twitter_link"], []) \
                                         .append({"game_name" : row["game_name"],
                                                  "game_url"  : row["game_url"]
                                                })

            self.dev_twitter_uid[row["main_twitter_link"]] = row["uid"]

    def send_messages(self):
        non_existent_users = []

        # For testing - sample developers who make multiple games
        # sample_dev_twitters = [key for key in self.dev_twitter_to_game_list.keys() if len(self.dev_twitter_to_game_list[key]) > 1][:5]
        
        sample_dev_twitters = sorted(self.dev_twitter_to_game_list.keys())
        sample_dev_twitters = sample_dev_twitters[self.start:self.end]

        for twitter_link in sample_dev_twitters:
            # extract Twitter user first
            username = twitter_link.split("/")[-1]
            logging.info("=====================Processing user " + username + "===================")
            logging.info("Games made by user " + username + " with uid: " + self.dev_twitter_uid[twitter_link])
            logging.info(self.dev_twitter_to_game_list[twitter_link])

            try :
                user = self.api.get_user(username)
                # user = self.api.get_user("vungocquang")

                logging.info("Sending message to user: " + username + " with Twitter user id: " + user.id_str)
                logging.info(self.compose_message(twitter_link, user.name))

                # self.api.send_direct_message(user.id_str, self.compose_message(twitter_link, user.name))
                # sleep_interval = random.uniform(21, 25)
                sleep_interval = random.uniform(1, 1)
                logging.info("Sleeping for " + str(sleep_interval) + " secs...")
                time.sleep(sleep_interval)

            except tweepy.TweepError as err:
                logging.warning(err, exc_info=True)
                non_existent_users.append({'user' : username, 
                                            'error': err.args[0][0]['message']
                                            })

    # Compose Twitter message to send
    def compose_message(self, twitter_link, user_name) -> str:

        base_url = "https://recommendindie.games/?itch_game="
        # base_url = "http://localhost:8080/?itch_game="
        username = twitter_link.split("/")[-1]

        # Retrieve all games developed by this developer
        game_list = self.dev_twitter_to_game_list[twitter_link]
        uid = self.dev_twitter_uid[twitter_link]
        # Get all game names developed by this developer
        all_game_names = ", ".join([x["game_name"] for x in game_list])

        # Build a list of customised links
        all_eva_links = []
        for game in game_list:
            dev = game["game_url"].split(".")[0]
            game_name = game["game_url"].split("/")[-1]
            all_eva_links.append(base_url + dev + "." + game_name + "&uid=" + uid)

        all_eva_links_str = " \n".join(all_eva_links)

        msg = "Dear " + user_name + " (@" + username + "),\n" + \
            "I am a Graduate student in the Analytics of Software, Games and Repository Data (ASGAARD) lab at University of Alberta. For my thesis project, I am working on a recommendation system for Itch.io games based on their similarity to best-selling Steam games. The goal is to help Indie developers with the discoverability of their games - there is no intent to monetize this system.\n" + \
            "I found your contact details from your Itch.io profile page and would like to invite you to give feedback on our recommendation system. For more official/formal information about the research, please refer to this document https://drive.google.com/file/d/1W_8QmKyJF5JOJuWQUGHXFyTyG_zuXihx/view?usp=sharing\n" + \
            "I found that you were involved in the development of the following "+ str(len(game_list)) + " game(s): " + all_game_names + ". I would like to ask you to evaluate our matches of each of your games to 5 - 15 popular Steam games. In each of the following links (each link corresponds to one of your Itch.io games), please rate all matches by clicking the Thumbs-up icon if you think the match is relevant (in terms of either plot contents, genres, gameplay, etc...) and Thumbs-down otherwise. Please also provide any feedback on the similarity and/or relevance:\n" + \
            all_eva_links_str + "\n" + \
            "Note that you can only evaluate the matches of your own games for now. Please keep in mind that this is a fun research project so the matches may be completely wrong or silly :) If so, do not hesitate to let us know via the 'comments' field on the website. We will use your feedback to try and improve the recommendation system.\n" + \
            "We would appreciate it if you could complete the rating within one week of receiving the invitation. Thank you and please let us know if you have any questions.\n" + \
            "Regards,\n" + \
            "Ngoc Quang Vu\n" + \
            "Graduate student\n" + \
            "ngocquan@ualberta.ca\n" + \
            "http://asgaard.ece.ualberta.ca\n"

        return msg

    def get_user_details(self, username):
        user = self.api.get_user(username)
        print("User details:")
        print(user.name)
        print(user.description)
        print(user.location)


def main():
    # Done 10 - 1800
    twitterMessenger = TwitterMessenger(1880, 1890)
    twitterMessenger.send_messages()
    

if __name__ == '__main__':
    main()
