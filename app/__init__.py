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
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def compare_select():
    macos_re = r'10\.\d+\..+\.txt'
    ls = os.listdir('.')
    versions = [os.path.splitext(file)[0] for file in ls if re.match(macos_re, file)]
    return render_template('select.html', versions=sorted(versions))

@app.route('/compare/<ver1>/<ver2>', methods=['GET'])
@app.route('/compare/<ver1>/<ver2>/<path:path>', methods=['GET'])
@app.route('/compare', methods=['POST'])
def compare_versions(ver1=None, ver2=None, path="", exclude=""):
    vers = []
    if request.method == "POST":
        ver1 = request.form["ver1"]
        ver2 = request.form["ver2"]
        path = request.form["path"]
        exclude = request.form["exclude"]

    for ver in ver1, ver2:
        try:
            with io.open(ver + '.txt', 'r', encoding='utf-8') as f:
                lines = []
                for line in f:
                    line = line.strip().lstrip('.')
                    if exclude and re.match(exclude, line):
                        continue
                    if line.startswith(path):
                        lines.append(line)
                ver_set = set(lines)
                vers.append(ver_set)
        except Exception as e:
            return str(e)

    files = sorted(list(vers[1] - vers[0]))
    return render_template('compare.html',
                           files=files,
                           ver1=ver1,
                           ver2=ver2,
                           path=path,
                           exclude=exclude)

if __name__ == '__main__':
    app.run()
