# -*- coding: utf-8 -*-
import os
import logging

basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books')
if not os.path.isdir(basedir):
    os.makedirs(basedir)

log_config = {
    'log_name': 'qu',
    'log_level': logging.DEBUG,
    'log_file': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qu.log')
}


