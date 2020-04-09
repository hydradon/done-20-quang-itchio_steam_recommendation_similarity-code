# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import os
from steamgamedetails.items import SteamgamedetailsItem
import pandas as pd

class StgamedetailsSpider(scrapy.Spider):
    name = 'stgamedetails'

    custom_settings = {
        'FEED_URI': "../dataset/top_steam_game_details_raw.csv",
        'FEED_FORMAT' : "csv"
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('topsteam_game_details.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    allowed_domains = ['steampowered.com']
    
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    df = pd.read_csv(os.path.join(project_dir + "/dataset", 'top_100_steam_games.csv'))

    start_urls = df["url"].tolist()

    def parse(self, response):
        item = SteamgamedetailsItem()

        item['game_name'] = response.css(".apphub_AppName ::text").extract_first("")
        item['game_url'] = response.url
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
