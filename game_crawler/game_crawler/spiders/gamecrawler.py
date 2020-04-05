# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
from game_crawler.items import GameCrawlerItem
import os
from html5print import HTMLBeautifier

class GamecrawlerSpider(scrapy.Spider):
    name = 'gamecrawler'

    custom_settings = {
        'FEED_URI': "../dataset/games_raw.csv",
        'FEED_FORMAT' : "csv"
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('game_crawler.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()

    allowed_domains = ['itch.io']
    base_url = 'https://www.itch.io'
    start_urls = [base_url + '/games?page=1']

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    def parse(self, response):
 
        for item in self.scrape(response):
            yield item

        #crawl next page
        next_page = response.xpath("//a[contains(text(), 'Next page')]/@href").extract_first("")
        if next_page:
            next_page_url = response.urljoin(next_page)
            print("Found url: {}".format(next_page_url))
            # input("Press to continue...")
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )

    def scrape(self, response):
        
        for game in response.css('.game_cell'):
            item = GameCrawlerItem()
            item['popular_page_no'] = response.url

            item['title'] = game.css(".game_cell_data .title ::text").extract_first("")
            item['url'] = game.css(".game_cell_data .title ::attr(href)").extract_first("")
            item['short_text'] = game.css(".game_text ::attr(title)").extract_first("")
            item['main_genre'] = game.css(".game_genre ::text").extract_first("")
            item['main_author'] = game.css(".game_author ::text").extract_first("")
            item['main_author_url'] = game.css(".game_author ::attr(href)").extract_first("")
            item['platforms'] = "||".join([plt.replace("Download for ", "") for plt in game.css(".game_platform ::attr(title)").extract()] + game.css(".game_platform .web_flag ::text").extract())
            item['platforms'] = item['platforms'].replace("Play in browser", "HTML5")

            yield item


