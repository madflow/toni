#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Toni, Toni, Toni
"""

import os
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs

APP_BASE_PATH = os.getcwd()

FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = os.path.join(APP_BASE_PATH, 'pages')
FREEZER_DESTINATION = os.path.join(APP_BASE_PATH, 'build')

FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'headerid', 'fenced_code'
                                 , 'footnotes']

app = Flask(__name__, static_folder=os.path.join(APP_BASE_PATH, 'static'
            ), template_folder=os.path.join(APP_BASE_PATH, 'templates'))
app.config.from_object(__name__)
pages = FlatPages(app)

@app.route('/')
def index():
    ordered = sorted(pages, reverse=False, key=lambda p: p.meta['order'
                     ])
    return render_template('index.html', pages=ordered)


@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page, pages=pages)


@app.route('/static/css/pygments.css')
def pygments_css():
    return (pygments_style_defs('tango'), 200,
            {'Content-Type': 'text/css'})
