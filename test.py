import pandas as pd
import os

game_overview = pd.read_csv("D:\\Research\\itchio-game\\dataset\\games_raw.csv")
all_game_urls = game_overview['url']

len(all_game_urls.drop_duplicates())
all_game_urls.drop_duplicates(inplace=True)

all_game_urls_list = all_game_urls.tolist()

html_dir = "D:\\Research\\itchio-game\\dataset_html"
filelist = []
for subdir, dirs, files in os.walk(html_dir):
    filelist.append(files)

fileSeries = pd.Series(filelist[0])

url_from_file = []
for filename in filelist[0]:
    author = filename.split(".")[0]
    game_name = filename.split(".")[1]
    url_from_file.append("https://" + author + ".itch.io/" + game_name)
