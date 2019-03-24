# -*- coding: utf-8 -*-
import scrapy
import re
import os
from os.path import getsize
from manga.items import episodeItem,imageItem
import manga.settings as st

def cleanLogs(log_path):
    if not os.path.exists(log_path):
        return
    with open(log_path,'w') as f:
        f.write('')

def cleanWrongFiles(root_dir):
    if not os.path.exists(root_dir):
        return
    for episode_dir in os.listdir(root_dir):
        print(episode_dir)
        x = root_dir + episode_dir+'/'
        print(os.walk(x))
        if os.path.isdir(x):
            for files in os.listdir(x):
                file_name = x+files
                print(file_name)
                if os.path.isfile(file_name) and getsize(file_name) == 0:
                    os.remove(file_name)
                    print('removed:',file_name)

class SuperSpider(scrapy.Spider):
    name = 'super'
    allowed_domains = ['manhua.fzdm.com']
    start_urls = ['http://manhua.fzdm.com/']

    def __init__(self):
        self.root_dir = st.ROOT_DIR+self.name+'/'
        self.exceptionlog = st.ROOT_DIR+self.name+st.LOG_FILE_NAME
        print(self.root_dir)
        if st.NEED_CLEAN_LOG == True:
            cleanLogs(self.exceptionlog)
        cleanWrongFiles(self.root_dir)
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
        image_url = response.xpath('//script[@type="text/javascript"]').re('mhurl="(.*?)"')[0]
        index = image_url.split('/')[0]
        image_item = imageItem()
        image_item['image_url'] = self.image_base_url1+image_url
        image_item['image_url_on_error'] = self.image_base_url0+image_url
        image_item['image_path'] = self.root_dir+item['dir_name']+'/'
        image_item['page_number'] = item['page_number']
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


