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
    if exists(folderpath) and isfile(folderpath + '/' + filename):
        return True
    else:
        return False


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
