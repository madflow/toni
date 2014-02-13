#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toni, Toni, Toni
"""

import argparse
import os

from flask_frozen import Freezer
from toni.app import app, APP_BASE_PATH
from toni.fs import copy_anything, create_temp_dir, delete_dir

DEBUG = True
DEFAULT_TEMPLATE = 'toni'
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),'templates')

def process_build(args):
    "Process the build"
    if(args.dir):
        if(os.path.isdir(args.dir)):
            target = args.dir
        else:
            target = os.path.join(APP_BASE_PATH, args.dir)
        app.config['FREEZER_DESTINATION'] = target
    freezer = Freezer(app)
    freezer.freeze()

def process_serve(args):
    app.run(port=args.port, debug=DEBUG)

def process_preview(args):
    args.dir = create_temp_dir()
    app.config['FREEZER_DESTINATION'] = args.dir
    process_build(args)
    print ' * Tempdir %s' % args.dir
    freezer = Freezer(app)
    freezer.serve(port=args.port)
    print' * Deleting %s' % args.dir
    delete_dir(args.dir)

def process_init(args):
    base_path = os.path.join(os.path.dirname(__file__),'..')
    target_path = args.dir
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    base_path = os.path.join(TEMPLATE_DIR, DEFAULT_TEMPLATE)
    pages = os.path.join(base_path, 'pages')
    templates = os.path.join(base_path, 'templates')
    static = os.path.join(base_path, 'static')

    copy_anything(pages, os.path.join(target_path ,'pages'))
    copy_anything(templates, os.path.join(target_path, 'templates'))
    copy_anything(static, os.path.join(target_path, 'static'))

def process_publish(args):
    pass


def main():
    parser = argparse.ArgumentParser(description='YO !!!')
    subparsers = parser.add_subparsers()
    
    init = subparsers.add_parser('init', 
        help='Initialize a project')
    init.add_argument('dir', help='The project directory')
    init.set_defaults(func=process_init)

    build = subparsers.add_parser('build', 
        help='Build static files')
    build.add_argument('--dir', help='The static files destination');
    build.set_defaults(func=process_build)

    publish = subparsers.add_parser('publish', 
        help='Publish static files to a remote server')
    publish.set_defaults(func=process_publish)

    serve = subparsers.add_parser('serve', 
        help='Start a development server')
    serve.add_argument('--port', default=8000, type=int)
    serve.set_defaults(func=process_serve)

    preview = subparsers.add_parser('preview', 
        help='Build and preview the build')
    preview.add_argument('--port', default=5000, type=int)
    preview.set_defaults(func=process_preview)

    args = parser.parse_args()
    args.func(args)
    