# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class episodeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dir_name = scrapy.Field()
    link_url = scrapy.Field()
    page_number = scrapy.Field()

class imageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dir_name = scrapy.Field()
    image_url = scrapy.Field()
    image_url_on_error = scrapy.Field()
    page_number = scrapy.Field()


