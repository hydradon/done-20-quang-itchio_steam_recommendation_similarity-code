# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
import os
import pandas as pd

class SteampagedlSpider(scrapy.Spider):
    name = 'steampagedl'

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('steampagedl.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

     # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    allowed_domains = ['steampowered.com']

    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    df = pd.read_csv(os.path.join(project_dir + "/dataset", 'top_500_steam_sellers_no_bundle.csv')) # correct one

    df.drop_duplicates(subset="game_name", ignore_index=True, inplace=True)

    start_urls = df["game_url"].tolist()

    def parse(self, response):
        url = response.url

        game_id = url.split("/")[4]
        game_name = url.split("/")[5]

        file_name = self.project_dir + "/dataset_html_steam/" + game_id + "." + game_name + ".html"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w+", encoding='utf-8-sig') as html_file:
            text = response.css(".page_content_ctn").extract_first(default = "")
            # html_file.write(HTMLBeautifier.beautify(text, 4))
            html_file.write(text)

        yield {
            'url': url
        }
