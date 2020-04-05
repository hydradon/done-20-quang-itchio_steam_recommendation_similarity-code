# -*- coding: utf-8 -*-
import scrapy
from twisted.python import log as twisted_log
import logging
from game_crawler.items import TagItem
import idna

class TagspiderSpider(scrapy.Spider):
    name = 'tagspider'

    custom_settings = {
        'FEED_URI': "../dataset/tag_raw.csv",
        'FEED_FORMAT' : "csv"
    }

    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('tag.log', 'w', 'utf-8-sig')])
    observer = twisted_log.PythonLoggingObserver()
    observer.start()
    # Allow URL with underscore to be crawled. For ex https://dj_pale.itch.io/unknown-grounds
    idna.idnadata.codepoint_classes['PVALID'] = tuple(
        sorted(list(idna.idnadata.codepoint_classes['PVALID']) + [0x5f0000005f])
    )

    allowed_domains = ['itch.io']
    base_url = 'https://www.itch.io'
    start_urls = [base_url + '/tags']

    def parse(self, response):
        for item in self.scrape(response):
            yield item

        #crawl next page
        next_page = response.css('.next_page ::attr(href)').extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            print("Found url: {}".format(next_page_url))
            # input("Press to continue...")
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )
    
    def scrape(self, response):
        for tag_cell in response.css(".tag_cell"):
            item = TagItem()

            item["title"] = tag_cell.css(".tag_title ::text").extract_first("")
            item["url"] = self.base_url + tag_cell.css(".tag_title ::attr(href)").extract_first("")
            item["related_tags"] = "||".join(tag_cell.css(".related_tags li ::text").extract())
            item["related_tags_url"] = "||".join([self.base_url + i for i in tag_cell.css(".related_tags a ::attr(href)").extract()])

            request = scrapy.Request(item['url'], callback=self.get_more_tag_details)
            request.meta['item'] = item #By calling .meta, we can pass our item object into the callback.
            yield request #Return the item + details back to the parser.

    def get_more_tag_details(self, response):
        item = response.meta['item']

        item["game_count"] = int(response.css(".game_count ::text").extract()[1].replace("results", "").replace(",", ""))
        item["short_text"] = response.css(".tag_description ::text").extract_first("")

        yield item
