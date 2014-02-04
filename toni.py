import argparse
import os
import shutil, errno

from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs

from flask_frozen import Freezer

app_folder = os.getcwd()

FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = os.path.join(app_folder, 'pages')
FREEZER_DESTINATION = os.path.join(app_folder, 'build')

FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'headerid', 'fenced_code', 'footnotes']

DEBUG = True

app = Flask(__name__, 
    static_folder=os.path.join(app_folder, 'static'), 
    template_folder=os.path.join(app_folder, 'templates'))
app.config.from_object(__name__)
pages = FlatPages(app)

@app.route('/')
def index():
    ordered = sorted(pages, reverse=False,
                    key=lambda p: p.meta['order'])
    return render_template('index.html', pages=ordered)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page, pages=pages)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}

def process_build(args):
    freezer = Freezer(app)
    freezer.freeze()

def process_serve(args):
    app.run(port=args.port, debug=DEBUG)

def process_preview(args):
    process_build(args)
    freezer = Freezer(app)
    freezer.serve(port=args.port)

def process_init(args):
    
    base_path = os.path.dirname(__file__)
    target_path = args.dir
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    pages = os.path.join(base_path, 'pages')
    templates = os.path.join(base_path, 'templates')
    static = os.path.join(base_path, 'static')

    copy_anything(pages, os.path.join(target_path ,'pages'))
    copy_anything(templates, os.path.join(target_path, 'templates'))
    copy_anything(static, os.path.join(target_path, 'static'))

def copy_anything(src, dst):
    '''
    http://stackoverflow.com/questions/1994488/copy-file-or-directory-in-python
    '''
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def process_publish(args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YO !!!')
    subparsers = parser.add_subparsers()

    init = subparsers.add_parser('init', help='Initialize a project')
    init.add_argument('dir', help='The project directory')
    init.set_defaults(func=process_init)

    build = subparsers.add_parser('build', help='Build static files')
    build.set_defaults(func=process_build)

    publish = subparsers.add_parser('publish', help='Publish static files to a remote server')
    publish.set_defaults(func=process_publish)

    serve = subparsers.add_parser('serve', help='Start a development server')
    serve.add_argument('--port', default=8000, type=int)
    serve.set_defaults(func=process_serve)

    preview = subparsers.add_parser('preview', help='Build and preview the build')
    preview.add_argument('--port', default=5000, type=int)
    preview.set_defaults(func=process_preview)

    args = parser.parse_args()
    args.func(args)

