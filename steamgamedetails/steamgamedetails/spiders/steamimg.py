# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import os
import glob
from steamgamedetails.items import ImageItem
import pandas as pd

class SteamimgSpider(scrapy.Spider):
    name = 'steamimg'

    custom_settings = {
        'ITEM_PIPELINES' : {
            'steamgamedetails.pipelines.CustomImageNamePipeline': 1,
        },
        'IMAGES_STORE' : "../dataset_imgs_steam",
        'DOWNLOAD_DELAY' : 0,
        "AUTOTHROTTLE_ENABLED" : False,
        "CONCURRENT_REQUESTS": 1024,
        "CONCURRENT_REQUESTS_PER_IP": 1024
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('steamimg.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    files = [f for f in glob.glob(project_dir + "/dataset_html_steam/*.html", recursive=True)]
    start_urls = ["file:///" + f for f in files]

    # start_urls = ["file:///D:/Research/itchio-game/dataset_html_steam/70.HalfLife.html"]

    def parse(self, response):
     
        img_url = response.css(".game_header_image_full ::attr(src)").extract_first("")

        file_name = response.url.replace("file:///", "").replace("%5C", "/").split("/")[4]
        game_id = file_name.split(".")[0]

        images = [{
            'url' : img_url,
            'name': game_id
        }]

        yield ImageItem(image_urls=images)
