# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import os, sys

app_path = os.path.dirname(                                       #/bookweb
        os.path.dirname(                                   #/crawler
            os.path.dirname(                               #/crawler
                os.path.dirname(                           #/spiders
                    os.path.abspath(__file__)))))#, 'app')  #xs_spider
sys.path.insert(0, app_path)

from app import create_app, db
from app.models import BookShelf

web_app = create_app('default')
web_app_context = web_app.app_context()
web_app_context.push()

bs_list = {} # Cache the BookShelf DB records
bs_books = {} # The map of bookselfs (name, and list of books under that shelf)
existing_books = set()
existing_book_urls = set()
crawled_books = set() #The history of crawled books with Name and URL
url_prefix = 'http://www.qu.la'

bookselfs = BookShelf.query.all()
for bs in bookselfs:
    bs_list[bs.shelf_name] = bs.id
    book_list = []
    for book in bs.books:
        existing_books.add(book.name)
        existing_book_urls.add(book.source_url)
        if not book.completed:
            book_list.append((book.id, book.name, book.source_url))

    bs_books[bs.shelf_name] = book_list


