# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
import os
from topsteamseller.items import TopsteamsellerItem

class TopsellerSpider(scrapy.Spider):
    name = 'topseller'

    custom_settings = {
        'FEED_URI': "../dataset/top_steam_sellers.csv",
        'FEED_FORMAT' : "csv"
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('top_steam_sellers.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    allowed_domains = ['steampowered.com']
    # start_urls = ['https://store.steampowered.com/search/?filter=topsellers&infinite=0']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers']

    def parse(self, response):
        for item in self.scrape(response):
            yield item

        #crawl next page
        change_page = response.xpath("//a[@class='pagebtn']/@href").extract()

        # Make sure to get the next page, not the previous page button
        next_page = change_page[1] if len(change_page) == 2 else change_page[0]

        if next_page:
            next_page_url = response.urljoin(next_page)
            print("Found url: {}".format(next_page_url))
            # input("Press to continue...")
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )

    def scrape(self, response):
        for row in response.css(".search_result_row"):
            item = TopsteamsellerItem()

            item['game_name'] = row.css(".title ::text").extract_first("")
            item['game_url'] = row.css("a ::attr(href)").extract_first("")
            item['game_release_date'] = row.css(".search_released ::text").extract_first("")

            yield item