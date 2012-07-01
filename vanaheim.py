#!/usr/bin/env python
#-*- encoding: utf-8 -*-

''' Vanaheim website engine '''

import yaml
from os.path import exists, isfile
# from os import pathsep
# from markdown import markdown
# from bottle import debug
from bottle import Bottle, run, jinja2_template as template
from bottle import static_file, HTTPError
import settings


VANAHEIM = Bottle()

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
    if hasattr(settings, 'MOVIES_PATH') else 'movies'
SLIDES_PATH = settings.SLIDES_PATH \
    if hasattr(settings, 'SLIDES_PATH') else 'slides'
PICS_PATH = settings.PICS_PATH \
    if hasattr(settings, 'PICS_PATH') else 'pics'
DL_PATH = settings.DL_PATH \
    if hasattr(settings, 'DL_PATH') else 'downloads'
STATIC_PATH = settings.STATIC_PATH \
    if hasattr(settings, 'STATIC_PATH') else 'static'
DISQUS_SHORTNAME = settings.DISQUS_SHORTNAME \
    if hasattr(settings, 'DISQUS_SHORTNAME') else ''

CTYPE_LIST = {'a': 'articles', 'b': 'breves', 's': 'static', 'w': 'slides'}


def get_file_contents(path, filename):
    ''' Description '''
    file_handle = open(path + filename, 'r')
    contents = file_handle.read().decode('utf-8')
    return contents


def extract_meta(contents):
    ''' Description '''
    print 'toto'


def gen_url(filename, ctype):
    ''' Define an url for a document using its filename and its access
    method'''
    basename = splitext(filename)[0]
    url = '/' + ctype + '/' + basename
    return url

def get_rule(ctype):
    ''' Description '''
    return 'articles'
    pass

@VANAHEIM.get('/')
def home():
    ''' Homepage definition '''
    return 'Hello!'


@VANAHEIM.get('/<ctype>/<name>')
def screen_contents(ctype, name):
    ''' Return some file contents using its name and metadatas '''
    try:
        folderpath = get_rule(ctype)
        src = open(folderpath + '/' + name + '.md','r')
        contents = src.readlines()
        src.close()
    except IOError:
        raise HTTPError(404, output='This post doesn\'t exist!')

    meta = []
    line = contents[0]

    while line !='\n':
        meta.append(contents.pop(0))
        line = contents[0]

    metadatas = yaml.load(''.join(meta))

    return metadatas


@VANAHEIM.get('/d/<filename:path>')
def download(filename):
    ''' Force download for files hosted in the downloads folder '''
    return static_file(filename, root=DL_PATH, download=filename)


@VANAHEIM.get('/s/<filename:path>')
def server_static(filename):
    ''' Give access to static files '''
    return static_file(filename, root=STATIC_PATH)


def main():
    ''' Run Vanaheim '''
    run(VANAHEIM, host='localhost', port=8080)
    return 0


if __name__ == '__main__':
    main()
