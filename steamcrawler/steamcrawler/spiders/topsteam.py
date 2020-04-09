# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import os
import pandas as pd
from steamcrawler.items import SteamcrawlerItem

class TopsteamSpider(scrapy.Spider):
    name = 'topsteam'

    custom_settings = {
        'FEED_URI': "../dataset/top_100_steam_games.csv",
        'FEED_FORMAT' : "csv"
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('pagedl.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    allowed_domains = ['steampowered.com']
    start_urls = ['https://store.steampowered.com/stats/']

    def parse(self, response):
        
        rows = response.css(".player_count_row")
        for row in rows:
            item = SteamcrawlerItem()
            item["name"] = row.css(".gameLink ::text").extract_first("")
            item["url"] = row.css(".gameLink ::attr(href)").extract_first("")
            item["num_players"] = int(row.css(".currentServers ::text").extract_first("0").replace(",", ""))
            yield item
            

        

