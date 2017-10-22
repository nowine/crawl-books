# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os, sys

app_path = os.path.dirname(                                #/bookweb
        os.path.dirname(                                   #/crawler
            os.path.dirname(                               #/crawler
                os.path.dirname(                           #/spiders
                    os.path.abspath(__file__)))))#, 'app')  #xs_spider
sys.path.insert(0, app_path)
