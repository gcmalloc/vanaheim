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


def check_exists(folderpath, filename):
    ''' Check if a file exists '''
    if exists(folderpath) and isfile(os.path.join(folderpath, filename)):
        return True
    else:
        return False


@VANAHEIM.get('/')
def home():
    ''' Homepage definition '''
    return 'Hello!'


@VANAHEIM.get('/<ctype:re:[vpsm]>/<fileid>')
def display_media(ctype, fileid):
    ''' Displays a media file, from its filename directly '''
    if ctype == 'v':
        fpath = settings.MOVIES_PATH
    elif ctype == 'm':
        fpath = settings.MUSIC_PATH
    elif ctype == 's':
        fpath = settings.STATIC_PATH
    elif ctype == 'p':
        fpath = settings.PICTURES_PATH
    else:
        raise HTTPError(404, output='This path doesn\'t exist!')
    return static_file(fileid, root=fpath)


@VANAHEIM.get('/d/<fileid>')
def download_file(fileid):
    ''' Download any media file from a direct url '''
    if check_exists(settings.STATIC_PATH, fileid):
        fpath = settings.STATIC_PATH
    elif check_exists(settings.MOVIES_PATH, fileid):
        fpath = settings.MOVIES_PATH
    elif check_exists(settings.MUSIC_PATH, fileid):
        fpath = settings.MUSIC_PATH
    elif check_exists(settings.PICTURES_PATH, fileid):
        fpath = settings.PICTURES_PATH
    else:
        raise HTTPError(404, output='This file doesn\'t exist!')
    return static_file(fileid, root=fpath, download=True)


@VANAHEIM.get('/<ctype:re:[ab]>/<fileid>')
def display_post(ctype, fileid):
    ''' Returns a post metadatas '''
    try:
        if ctype == 'a':
            folderpath = settings.SITE_PATH + 'articles'
        elif ctype == 'b':
            folderpath = settings.SITE_PATH + 'breves'
        else:
            raise HTTPError(404, output='This path doesn\'t exist!')
        src = open(os.join(folderpath, fileid) + '.md', 'r')
        contents = src.readlines()
        src.close()
    except IOError:
        raise HTTPError(404, output='This post doesn\'t exist!')
    meta = []
    line = contents[0]
    while line != '\n':
        meta.append(contents.pop(0))
        line = contents[0]
    metadatas = yaml.load(''.join(meta))
    return metadatas


@VANAHEIM.error(403)
@VANAHEIM.error(404)
@VANAHEIM.error(500)
def errors(code):
    ''' Error management '''
    return template("templates/error.html", code=code)


def main():
    ''' Run Vanaheim '''
    run(VANAHEIM, host='localhost', port=8080, reloader=True)
    return 0


if __name__ == '__main__':
    main()
