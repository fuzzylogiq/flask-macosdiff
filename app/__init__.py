#!/usr/bin/env python
# encoding: utf-8
"""
macosdiff.py

This is a Flask app to show you the differences between the files installed by
two different versions of the macOS installer.

Copyright (C) University of Oxford 2018
    Ben Goodstein <ben.goodstein at it.ox.ac.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import io
import os
import os.path
import re
import gzip
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from joblib import Memory

cachedir = '.cache'
datadir = 'data'
memory = Memory(cachedir, verbose=11, compress=9)

app = Flask(__name__)
Bootstrap(app)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

@app.route('/')
def compare_select():
    versions = []
    macos_re = r'(?P<version>10\.\d+\..+)\.txt\.gz'
    ls = os.listdir(datadir)
    for filename in ls:
        m = re.match(macos_re, filename)
        if m:
            versions.append(m.groupdict()['version'])
    print versions
    return render_template('select.html', versions=sorted(versions, key=natural_keys))

@memory.cache
def diff(ver1, ver2, path="", exclude=""):
    vers = []
    for ver in ver1, ver2:
            try:
                with gzip.open(datadir + '/' + ver + '.txt.gz', 'r') as f:
                    lines = []
                    for line in f:
                        line = line.decode('utf-8')
                        line = line.strip().lstrip('.')
                        if exclude and re.match(exclude, line):
                            continue
                        if line.startswith(path):
                            lines.append(line)
                    ver_set = set(lines)
                    vers.append(ver_set)
            except Exception as e:
                raise(e)

    return sorted(list(vers[1] - vers[0]))

@app.route('/compare/<ver1>/<ver2>', methods=['GET'])
@app.route('/compare/<ver1>/<ver2>/<path:path>', methods=['GET'])
@app.route('/compare', methods=['POST'])
def compare_versions(ver1=None, ver2=None, path="", exclude=""):
    if request.method == "POST":
        ver1 = request.form["ver1"]
        ver2 = request.form["ver2"]
        path = request.form["path"]
        exclude = request.form["exclude"]

    files = diff(ver1, ver2, path, exclude)
    return render_template('compare.html',
                           files=files,
                           ver1=ver1,
                           ver2=ver2,
                           path=path,
                           exclude=exclude)

if __name__ == '__main__':
    app.run()
