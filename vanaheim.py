#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import logging
import re
from os.path import splitext
import markdown

import settings

# Get the settings from settings.py
# if not attibuted in settings.py, set variable to nil
BLOG_TITLE = settings.BLOG_TITLE \
    if hasattr(settings, "BLOG_TITLE") else ""
BLOG_SUBTITLE = settings.BLOG_SUBTITLE \
    if hasattr(settings, "BLOG_SUBTITLE") else ""
POSTS_PER_PAGE = settings.POSTS_PER_PAGE \
    if hasattr(settings, "POSTS_PER_PAGE") else 10
SUMMARY_DELIMITER = settings.SUMMARY_DELIMITER \
    if hasattr(settings, "SUMMARY_DELIMITER") else "~~~"
DISQUS_SHORTNAME = settings.DISQUS_SHORTNAME \
    if hasattr(settings, "DISQUS_SHORTNAME") else ""


def gen_url(filename):
    """ Define an url for a document using its filename and its type """
    basename = splitext(filename)[0]
