#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Publishers
Credits: https://github.com/hyde/hyde/blob/master/hyde/ext/publishers/dvcs.py
"""

from subprocess import Popen, PIPE

class Git(object):

    path = None
    branch = 'master'

    def __init__(self, path):
        self.path = path

    def add(self, path='.'):
        cmd = Popen('git add "%s"' % path, cwd=unicode(self.path),
                    stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)

    def pull(self, branch):
        self.switch(self.branch)
        cmd = Popen('git pull origin %s' % branch,
                    cwd=unicode(self.path), stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)

    def push(self, branch):
        cmd = Popen('git push origin %s' % branch,
                    cwd=unicode(self.path), stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)

    def commit(self, message):
        cmd = Popen('git commit -a -m"%s"' % message,
                    cwd=unicode(self.path), stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)

    def switch(self, branch):
        self.branch = branch
        cmd = Popen('git checkout %s' % branch, cwd=unicode(self.path),
                    stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)

    def merge(self, branch):
        cmd = Popen('git merge %s' % branch, cwd=unicode(self.path),
                    stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)

    def clone(self, repo):
        cmd = Popen('git clone %s %s' % (repo, self.path), cwd=unicode(self.path),
                    stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)

    def empty(self):
        cmd = Popen('git rm -r *', cwd=unicode(self.path),
                    stdout=PIPE, shell=True)
        cmdresult = cmd.communicate()[0]
        if cmd.returncode:
            raise Exception(cmdresult)