# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TopsteamsellerItem(scrapy.Item):
    # define the fields for your item here like:
    game_name = scrapy.Field()
    game_url = scrapy.Field()
    game_release_date = scrapy.Field()
