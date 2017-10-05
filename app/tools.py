# -*- coding: utf-8 -*-

import requests

base_url = 'http://www.qu.la/book/{:05d}'

def init_full_load(base=base_url):
    urls = (base.format(x) for x in range(99999))
    for url in urls:
        crawl_book_page(url)


def daily_update(base=base_url):
    pass


def crawl_book_page(url):
    pass


def crawl_new_chapter(url):
    pass


def crawl_chapter_page(url):
    pass


def save_book():
    pass


def save_chapter():
    pass
