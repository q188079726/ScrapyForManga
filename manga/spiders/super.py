# -*- coding: utf-8 -*-
import scrapy
import re
import os
from os.path import getsize
from manga.items import episodeItem,imageItem

class SuperSpider(scrapy.Spider):
    name = 'super'
    allowed_domains = ['manhua.fzdm.com']
    start_urls = ['http://manhua.fzdm.com/']

    def __init__(self):
        self.image_base_url0 = 'http://p0.xiaoshidi.net/'
        self.image_base_url1 = 'http://p1.xiaoshidi.net/'

    def parse(self,response):
        link_urls = response.xpath('//li[@class="pure-u-1-2 pure-u-lg-1-4"]/a/@href').extract()
        titles = response.xpath('//li[@class="pure-u-1-2 pure-u-lg-1-4"]/a/@title').extract()
        for index in range(len(link_urls)):
            item = episodeItem()
            url = self.start_urls[0]+link_urls[index]
            item['link_url'] = url
            item['dir_name'] = titles[index]
            item['page_number'] = 'index_0.html' 
            yield scrapy.Request(url,meta={'item':item},callback=self.parseEpisodePage)
            
    def parseEpisodePage(self,response):
        item = response.meta['item']   
        image_item = imageItem()
     
        image_url = response.xpath('//script[@type="text/javascript"]').re('mhurl="(.*?)"')[0]
        
        image_item['dir_name'] = item['dir_name']
        image_item['image_url'] = self.image_base_url1+image_url
        image_item['image_url_on_error'] = self.image_base_url0+image_url
        image_item['page_number'] = re.search(r'index_(.*)\.html',item['page_number']).group(1) +'.jpg'
        
        yield image_item

        nextPage = response.xpath('//link[@rel="prefetch"]/@href').extract()
        if nextPage: 
            pagenumber = nextPage[0].split('/')[-1]
            new_item = episodeItem()
            new_item['dir_name'] = item['dir_name']
            new_item['link_url'] = item['link_url']
            new_item['page_number'] = pagenumber
            url = item['link_url']+nextPage[0]
            yield scrapy.Request(url,meta={'item':new_item},callback=self.parseEpisodePage)
