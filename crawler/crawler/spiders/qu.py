# -*- coding: utf-8 -*-

import os
import sys
import re
import logging
import requests
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .config import basedir, log_config
from ..items import BookItem

from app import create_app, db
from app.models import Book, Chapter

def get_book_folder_path(book_id):
    book_id = str(book_id)
    book_folder = os.path.join(basedir, book_id)
    if not os.path.isdir(book_folder):
        os.mkdir(book_folder)

    return book_folder


def re_filters(original):
    cleaners = [
        re.compile(r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I),
        re.compile(r'<\s*div[^>]*>', re.I),
        re.compile(r'<\s*/\s*div\s*>', re.I)
    ]
    for clr in cleaners:
        original = clr.sub("", original)

    return original


def char_filters(original):
    original = original.replace('\u3000', "")
    original = original.replace('\r', "")
    original = original.replace('\n', "")
    original = original.replace('\t', "")
    last_br = original.lower().rfind('br>')
    return original[:last_br+3]


def get_book_detail(name, author):
    search_url = "https://www.qidian.com/search"
    payload = {'kw': name, }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(search_url, params=payload, headers=headers)

    soap = BeautifulSoup(response.content, 'html5lib')
    book_divs = soap.find_all('div', class_='book-mid-info')
    for book in book_divs:
        book_name = book.h4.a.text
        book_author = book.find(class_='author').a.text
        book_status = book.find(class_='author').span.text
        book_intro = book.find(class_='intro').text
        book_cat = book.find(attrs={'data-eid': 'qd_S07'}).text
        if book_author == author and book_name == name:
            target_book = {
                'name': book_name,
                'author': book_author,
                'status': book_status,
                'intro': book_intro,
                'category': book_cat
            }
            return target_book

    return None


def init_logger(logger_name, logger_level, logger_file):
    logger = logging.getLogger(logger_name)
    fmt = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler(logger_file)
    file_handler.setFormatter(fmt)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logger_level)
    return logger


class QuSpider(CrawlSpider):
    name = 'qu'
    #allowed_domains = ['http://www.qu.la']
    #start_urls = ('http://www.qu.la/book/{:05d}/'.format(x) for x in range(1, 2))
    start_urls = ['http://www.qu.la/book/46030/']

    rules = (
        Rule(LinkExtractor(allow=(r'http://www.qu.la/book/\d+/\d+\.html',)), callback="parse_chapter"),
    )

    def __init__(self, *args, **kwargs):
        super(QuSpider, self).__init__(*args, **kwargs)
        self.web_app = create_app('default')
        self.web_app_context = self.web_app.app_context()
        self.web_app_context.push()


    def closed(self, reason):
        self.web_app_context.pop()
        #super(QuSpider, self).closed(reason)


    def parse_start_url(self, response):
        try:
            name = response.xpath("//div[@class='box_con']/div[@id='maininfo']/div[@id='info']/h1/text()")[0].extract()
            author = response.xpath("//div[@class='box_con']/div[@id='maininfo']/div[@id='info']/p/text()")[0].extract().split("：")[1]
            summary = response.xpath("//div[@class='box_con']/div[@id='maininfo']/div[@id='intro']/text()")[0].extract()
        except IndexError as e:
            self.logger.info('Failed to extract key data of %s', response.url)
            return None

        self.logger.info('Name: %s, Author: %s, Summary %s', name, author, summary)
        book = get_book_detail(name, author)
        if book:
            self.logger.info(book)

        return None


    def parse_chapter(self, response):
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        book_id = response.url.split('/')[-2]
        chapter_id = response.url.split('/')[-1]
        self.logger.info('Book_ID: %s, Chapter_id: %s', book_id, chapter_id)
        chapter_name = response.xpath("//div[@class='bookname']/h1/text()")[0].extract()
        chapter_content = response.xpath("//div[@id='content']").extract()[0]
        chapter_content = re_filters(chapter_content)
        chapter_content = char_filters(chapter_content)
        book_folder = get_book_folder_path(book_id)
        self.logger.info(book_folder)
        file_path = os.path.join(book_folder, chapter_id)
        self.logger.info(file_path)
        with open(file_path, 'w') as f:
            f.write(chapter_content)


