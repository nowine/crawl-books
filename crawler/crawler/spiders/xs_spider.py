# -*- coding: utf-8 -*-

import os, sys
import scrapy
from lxml import etree

#app_path = os.path.join(
app_path = os.path.dirname(                                       #/bookweb
        os.path.dirname(                                   #/crawler
            os.path.dirname(                               #/crawler
                os.path.dirname(                           #/spiders
                    os.path.abspath(__file__)))))#, 'app')  #xs_spider
print(app_path)
sys.path.insert(0, app_path)
print(sys.path)

from app import create_app, db
from app.models import Chapter

class XS_Spider(scrapy.Spider):
    name = "XiaoShuo"

    def __init__(self, *args, **kwargs):
        super(XS_Spider, self).__init__(*args, **kwargs) #Call default init of parent class
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def start_requests(self):
        urls = ["http://www.33xs.com/33xs/254/254902/13101092.html", ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.log(result_dir)
        page = response.url.split("/")[-1]
        self.log(page)
        self.log(filename)
        bodystr = response.body.decode("gbk").rstrip('&#13;')
        #print(bodystr)
        html = etree.HTML(bodystr)
        detail = html.xpath('//div[@id ="detail"]')
        if detail and len(detail) > 0:
            chapter_content =etree.tounicode(detail[0])
            chapter_title = "楔子"
            c = Chapter(title=chapter_title, content=chapter_content)
            db.session.add(c)
            db.session.commit()

    def clear_up(self):
        pass  # to clear_up the
