# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import os
import glob
from steamgamedetails.items import SteamgamedetailsItem
import pandas as pd

class StgamedetailsSpider(scrapy.Spider):
    name = 'stgamedetails'

    custom_settings = {
        'FEED_URI': "../dataset/top_500_steam_sellers_details_raw.csv",
        'FEED_FORMAT' : "csv",
        'DOWNLOAD_DELAY' : 0,
        "AUTOTHROTTLE_ENABLED" : False,
        "CONCURRENT_REQUESTS": 1024,
        "CONCURRENT_REQUESTS_PER_IP": 1024
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('topsteam_game_details.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    allowed_domains = ['steampowered.com']
    
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # df = pd.read_csv(os.path.join(project_dir + "/dataset", 'top_steam_sellers.csv'))
    # df.drop_duplicates(subset="game_name", ignore_index=True, inplace=True)
    # start_urls = df["game_url"].tolist()

    files = [f for f in glob.glob(project_dir + "/dataset_html_steam/*.html", recursive=True)]
    start_urls = ["file:///" + f for f in files]
   
    def parse(self, response):
        item = SteamgamedetailsItem()

        file_name = response.url.replace("file:///", "").replace("%5C", "/").split("/")[4]
        game_id = file_name.split(".")[0]
        game_name = file_name.split(".")[1]

        item['game_name'] = response.css(".apphub_AppName ::text").extract_first("")

        # https://store.steampowered.com/app/239140/Dying_Light/
        item['game_url'] = "https://store.steampowered.com/app/" + game_id + "/" + game_name
        item['game_tags'] = "||".join([i.strip() for i in response.css(".popular_tags .app_tag ::text").extract()])

        game_details_blk = response.css(".details_block")[0]
        item['game_genres'] = "||".join(game_details_blk.xpath("//*[contains(text(), 'Genre')]/following-sibling::a/text()").extract())
        item['game_desc_snippet'] = response.css(".game_description_snippet ::text").extract_first("").strip()
        
        LONG_DESC_SELECTOR = "//*[@class='game_area_description']/descendant-or-self::text()"
        long_description = [i.strip() for i in response.xpath(LONG_DESC_SELECTOR).extract() 
                                if i.strip() 
                                and i.casefold() != "about this game"]
        item['game_desc'] = " ".join(long_description)

        yield item
