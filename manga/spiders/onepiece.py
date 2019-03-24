# -*- coding: utf-8 -*-
import scrapy
import os
from manga.spiders.super import SuperSpider

class OnepieceSpider(SuperSpider):
    name = 'onepiece'
    start_urls = ['http://manhua.fzdm.com/2/']

    def __init__(self):
        super(OnepieceSpider,self).__init__()

