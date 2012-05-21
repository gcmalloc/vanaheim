#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import logging
import re
from os.path import splitext
from markdown import markdown
from bottle import Bottle, run, jinja2_template as template
from bottle import static_file
import settings


vanaheim = Bottle()

# Get the settings from settings.py
# if not attibuted in settings.py, set variable to nil
SITE_TITLE = settings.SITE_TITLE \
    if hasattr(settings, 'SITE_TITLE') else ''
SITE_SUBTITLE = settings.SITE_SUBTITLE \
    if hasattr(settings, 'SITE_SUBTITLE') else ''
POSTS_PER_PAGE = settings.POSTS_PER_PAGE \
    if hasattr(settings, 'POSTS_PER_PAGE') else 10
SUMMARY_DELIMITER = settings.SUMMARY_DELIMITER \
    if hasattr(settings, 'SUMMARY_DELIMITER') else '~~~'
SITE_PATH = settings.SITE_PATH \
    if hasattr(settings, 'SITE_PATH') else ''
MOVIES_PATH = settings.MOVIES_PATH \
    if hasattr(settings, 'MOVIES_PATH') else ''
PICS_PATH = settings.PICS_PATH \
    if hasattr(settings, 'PICS_PATH') else ''
DL_PATH = settings.DL_PATH \
    if hasattr(settings, 'DL_PATH') else ''
DISQUS_SHORTNAME = settings.DISQUS_SHORTNAME \
    if hasattr(settings, 'DISQUS_SHORTNAME') else ''

def get_file_contents(path,filename):
    file_handle = open(path + filename, 'r')
    contents = file_handle.read().decode('utf-8')
    return contents

def extract_meta(contents):
    print 'toto'
    

def gen_url(filename, letter):
    ''' Define an url for a document using its filename and its type '''
    basename = splitext(filename)[0]
    url = '/'+letter+'/'+basename
    return url

@vanaheim.get('/')
def home():
    ''' Homepage definition '''
    return 'Hello'

@vanaheim.get('/d/<filename:path>')
def download(filename):
    ''' Force download for files hosted in the downloads folder '''
    return static_file(filename, root=DL_PATH, download=filename)

def main():
    ''' Run Vanaheim '''
    run(vanaheim, host='localhost', port=8080)
    return 0

if __name__ == '__main__':
    main()
