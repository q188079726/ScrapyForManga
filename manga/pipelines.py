# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
import settings as st
class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_url = item.get('image_url')
        if image_url:
            yield scrapy.Request(image_url,meta={'item':item})
        else:
            return

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        episode_dir = item.get('dir_name')
        dir = os.path.join(st.IMAGES_STORE,episode_dir) 
        if not os.path.exists(dir):
            os.makedirs(dir)
        image_name = item.get('page_number')
        image_path = os.path.join(episode_dir,image_name)
        return image_path


