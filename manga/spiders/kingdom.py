# -*- coding: utf-8 -*-
import scrapy
import os
from manga.spiders.super import SuperSpider

class KingdomSpider(SuperSpider):
    name = 'kingdom'
    start_urls = ['https://manhua.fzdm.com/74/']

    def __init__(self):
        super(KingdomSpider,self).__init__()
