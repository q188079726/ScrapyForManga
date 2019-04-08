# -*- coding: utf-8 -*-
import scrapy
from manga733.items import Manga733Item
import re

class BasketballSpider(scrapy.Spider):
    name = 'basketball'
    allowed_domains = ['733.so','img_733.234us.com']
    start_urls = ['http://www.733.so/mh/22539/']
    base_url = 'http://www.733.so'

    def parse(self, response):
        chapter_url_list = response.xpath('//div[@class="cy_plist"]/ul/li/a/@href').extract()
        chapter_name_list = response.xpath('//div[@class="cy_plist"]/ul/li/a/p/text()').extract()
        for i,url in enumerate(chapter_url_list):
        # for i in range(2):
            # url = chapter_url_list[i]
            chapter_name = chapter_name_list[i]
            req = scrapy.Request(self.base_url+url,callback=self.parse_chapter)
            req.chapter_name = chapter_name
            yield req

    def parse_chapter(self,response):
        chapter_url = response.url
        req = response.request
        #先循环所有页
        total_page = response.xpath('//span[@id="k_total"]/text()').extract()
        for i in range(1,int(total_page[0])+1):
        # for i in range(1,3):
            url  = chapter_url+'?p='+str(i)
            new_request = scrapy.Request(url,callback=self.parse_page)
            new_request.chapter_name = req.chapter_name
            new_request.page_num = str(i)
            yield new_request
        

    def parse_page(self,response):
        req = response.request
        item = Manga733Item()
        image_url = response.xpath('//tr/td/img/@src').extract()
        item['image_chapter_name'] = req.chapter_name
        item['image_page_number'] = req.page_num
        item['image_url'] = image_url[0]
        yield item