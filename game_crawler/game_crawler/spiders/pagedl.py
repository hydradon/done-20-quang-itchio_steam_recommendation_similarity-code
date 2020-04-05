# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import idna
import os
import pandas as pd

class PagedlSpider(scrapy.Spider):
    name = 'pagedl'

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('pagedl.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    allowed_domains = ['itch.io']

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    df = pd.read_csv(os.path.join(root_dir + "/dataset", 'games_raw.csv'))

    crawl_urls = df["url"].tolist()

    start_urls = ['https://itch.io/login']

    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        return [scrapy.FormRequest.from_response(response,
                                                 formdata={'csrf_token': token,
                                                           'username': 'hydradon', #TODO use own usename and pass!
                                                           'password': 'nosalis9)'},
                                                 formcss='.login_form_widget .form',
                                                 callback=self.check_login_response)]

    def check_login_response(self, response):
        if b"Incorrect username or password" in response.body:
            self.log("Login failed", level=logging.ERROR)
            return
        else:
            self.log("Successfully logged in!!")
            for url in self.crawl_urls:
                yield scrapy.Request(url=url, callback=self.scrape)                                           
       
    def scrape(self, response):
        url = response.url

        # https://whilefun.itch.io/brick-breaker-remix
        developer = response.url.split("/")[2].split(".")[0] # whilefun
        game_name = response.url.split("/")[3] # brick-breaker-remix

        file_name = self.root_dir + "/dataset_html/" + developer + "." + game_name + ".html"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w+", encoding='utf-8-sig') as html_file:
            text = response.css(".main").extract_first(default = "")
            # html_file.write(HTMLBeautifier.beautify(text, 4))
            html_file.write(text)

        yield {
            'url': url
        }
