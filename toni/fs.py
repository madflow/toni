#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filesystem helpers
"""

import shutil
import errno
from tempfile import mkdtemp
import os

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

def create_temp_dir():
    ''' Creates a temporary directory'''
    return mkdtemp()

def delete_dir(path):
    return shutil.rmtree(path)