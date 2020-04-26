# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class SteamgamedetailsPipeline(object):
    def process_item(self, item, spider):
        return item


class CustomImageNamePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image in item.get('image_urls', []):
            yield scrapy.Request(image["url"], meta={'image_name': image["name"]})

    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['image_name']