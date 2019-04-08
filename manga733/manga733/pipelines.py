# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
import requests

class Manga733Pipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_url = item.get('image_url')
        resp = requests.get(image_url)
        print(resp.url)
        item['image_url'] = resp.url
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referrer Policy': 'no-referrer-when-downgrade'
        }

        response = requests.get(resp.url,headers = header,timeout=3)
        d = item.get('image_chapter_name')
        p = item.get('image_page_number')
        root = os.path.join(os.path.expanduser("~"), 'Pictures','basketball')
        dirc = os.path.join(root,d)
        if not os.path.exists(dirc):
            os.mkdir(dirc)
        fp = os.path.join(dirc,p+'.jpg')
        with open(fp,'wb') as f:
                f.write(response.content)
        return None


