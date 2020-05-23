# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import os
import glob
from game_crawler.items import DevContactItem
import pandas as pd

class DevinfoSpider(scrapy.Spider):
    name = 'devinfo'

    custom_settings = {
        'FEED_URI': "../dataset/itch_dev_contacts.csv",
        'FEED_FORMAT' : "csv",
        'DOWNLOAD_DELAY' : 0,
        "AUTOTHROTTLE_ENABLED" : False,
        "CONCURRENT_REQUESTS": 1024,
        "CONCURRENT_REQUESTS_PER_IP": 1024
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('dev_contacts.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()
    
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    files = [f for f in glob.glob(project_dir + "/dataset_itch_dev_html/*.html", recursive=True)]
    start_urls = ["file:///" + f for f in files]

    def parse(self, response):

        item = DevContactItem()

        file_name = response.url.replace("file:///", "").replace("%5C", "/").split("/")[4]
        item["game_developers_url"] = "https://" + file_name.replace(".html", "") + ".itch.io"


        user_links = set(url.rstrip("/") for url in response.css(".user_links a ::attr(href)").extract())
        main_twitter = set([s.replace("http:", "https:") for s in user_links if "twitter.com/" in s])
        item["main_twitter_link"] = "||".join(main_twitter) if len(main_twitter) > 0 else ""


        all_links = set(url.rstrip("/").replace("http:", "https:") for url in response.css(".profile_column a ::attr(href)").extract()) - main_twitter

        profile_link = set([s for s in all_links if "itch.io/profile" in s])
        item["profile_link"] = "||".join(profile_link) if len(profile_link) > 0 else ""

        twitter = set([s for s in all_links if "twitter.com/" in s])
        item["twitter_links"] = "||".join(twitter) if len(twitter) > 0 else ""

        facebook = set([s for s in all_links if "facebook.com/" in s])
        item["facebook_links"] = "||".join(facebook) if len(facebook) > 0 else ""

        discord = set([s for s in all_links if "discord.com/" in s])
        item["discord_links"] = "||".join(discord) if len(discord) > 0 else ""

        emails = set([s for s in all_links if "mailto:" in s])
        item["emails"] = "||".join(emails) if len(emails) > 0 else ""

        other_links = all_links - profile_link - twitter - facebook - discord - emails
        item["other_links"] = "||".join(other_links) if len(other_links) > 0 else ""


        yield item