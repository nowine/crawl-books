# -*- coding: utf-8 -*-

import os
import scrapy

from config import basedir
from app import create_app, db
from app.models import Chapter, BookShelf, Book
from .items import BookItem


def get_book_folder_path(book_id):
    book_id = str(book_id)
    main_folder = os.path.join(basedir, 'books')
    book_folder = os.path.join(main_folder, book_id)
    if not os.path.isabs(book_folder):
        os.mkdir(book_folder)
    return book_folder


class BaseSpider(scrapy.Spider):
    '''
    The base spider created to built the shared app context, e.g. initiate flask
    app instance so that initiate the DB instance.
    Benefit, if in future I want to built split the book records in separate DB,
    I can just amend to code here. I think I need to split it, because the books
    will be stored in static pages, so it is not necessary to have those tables in
    app`s DB. But at this moment, just make it easier for my work
    '''
    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.web_app = create_app(xs_config.app_config)
        self.web_app_context = self.web_app.app_context()
        self.web_app_context.push()

    def closed(self, reason):
        #release the app_context and other resources if any
        self.web_app_context.pop()
        super(BaseSpider, self).closed(reason)


class QuSpider(BaseSpider):
    name = 'qu'
    allowed_domains = ['http://www.qu.la']
    base_url = 'http://www.qu.la/{:05d}'
    start_urls = (base_url.format(x) for x in range(3))

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        bi = BookItem()
        bi['name'] = response.xpath("//div[@class='box_con']/div[@id='maininfo']/div[@id='info']/h1/text()")[0].extract()
        bi['author'] = response.xpath("//div[@class='box_con']/div[@id='maininfo']/div[@id='info']/p/text()")[0].extract().split(":")[1]
        bi['summary'] = response.xpath("//div[@class='box_con']/div[@id='maininfo']/div[@id='intru']/text()")[0].extract()
        return bi


    def parse_chapters(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
