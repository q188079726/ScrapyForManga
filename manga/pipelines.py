# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import re

class MangaPipeline(object):
    def process_item(self, item, spider):
        if 'image_url' in item:
            path = item['image_path']
            file_name = path + re.search(r'index_(.*)\.html',item['page_number']).group(1) +'.jpg'
            print("********++++++++")
            print(item)
            print("********++++++++")
            url = item['image_url']
            if not os.path.exists(path):
                os.makedirs(path)
            if os.path.exists(file_name):
                print('jump with:',file_name)
                return item
            print('\033[1;32;40m')
            print('downloading:',url,'to:',file_name)
            print('\033[0m')
            header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Referrer Policy':'no-referrer-when-downgrade'}
            try:
                response = requests.get(url,headers = header,timeout=5)
            except Exception as e:
                print(e)
            finally:
                url = item['image_url_on_error']
                print('\033[1;33;40m')
                print('downloading:',url,'to:',file_name)
                print('\033[0m')
                try: 
                    response = requests.get(url,headers = header,timeout=5)
                except Exception as e:
                    print('\033[1;31;40m')
                    print('404 404 404 404 404 404 404 404 ')
                    print(e)
                    print('\033[0m')
                    with open(spider.exceptionlog,'a') as f:
                        f.write(str(item)+e+'\n\n')
                    return item
            print('\033[1;33;40m')
            print('saving image:',response.headers)
            print('\033[0m')
            with open(file_name,'wb') as f:
                f.write(response.content)
        return item
