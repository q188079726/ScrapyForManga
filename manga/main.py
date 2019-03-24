from scrapy.cmdline import execute
import os
import sys

#添加当前项目的绝对地址
path = os.path.dirname(os.path.abspath(__file__))
print(path)
sys.path.append(path)
spider_name = 'onepiece' 
#执行 scrapy 内置的函数方法execute，  使用 crawl 爬取并调试，最后一个参数jobbole 是我的爬虫文件名
try:
    execute(['scrapy', 'crawl', spider_name])
except Exception as e:
    print(e)
