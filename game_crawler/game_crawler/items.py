# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GameCrawlerItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    short_text = scrapy.Field()
    main_genre = scrapy.Field()
    main_author = scrapy.Field()
    main_author_url = scrapy.Field()
    platforms = scrapy.Field()
    popular_page_no = scrapy.Field()

class GameDetailsItem(scrapy.Item):

    game_name = scrapy.Field()
    game_developers = scrapy.Field()
    game_developers_url = scrapy.Field()
    game_url = scrapy.Field()
    game_price = scrapy.Field()

    game_last_update = scrapy.Field()
    game_publish_date = scrapy.Field()
    game_release_date = scrapy.Field()

    game_desc = scrapy.Field()
    game_desc_len = scrapy.Field()
    game_no_screenshots = scrapy.Field()

    game_status = scrapy.Field()
    game_platforms = scrapy.Field()
    game_genres = scrapy.Field()
    game_tags = scrapy.Field()
    game_made_with = scrapy.Field()
    game_ave_session = scrapy.Field()
    game_language = scrapy.Field()
    game_inputs = scrapy.Field()
    game_accessibility = scrapy.Field()
    game_source_code = scrapy.Field()
    game_license = scrapy.Field()
    game_asset_license = scrapy.Field()
    
    game_criteria = scrapy.Field()

    game_no_ratings = scrapy.Field()
    game_rating = scrapy.Field()

    game_multiplayer = scrapy.Field()
    game_mentions = scrapy.Field()
    game_links = scrapy.Field()

    game_size = scrapy.Field()
    
    
class TagItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    short_text = scrapy.Field()
    related_tags = scrapy.Field()
    related_tags_url = scrapy.Field()
    game_count = scrapy.Field()