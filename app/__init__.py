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
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def you_found_me():
    return 'You found me!'

@app.route('/compare/<ver1>/<ver2>')
@app.route('/compare/<ver1>/<ver2>/<path:path>')
def compare_versions(ver1, ver2, path=None):
    vers = []
    for ver in ver1, ver2:
        try:
            with io.open(ver + '.txt', 'r', encoding='utf-8') as f:
                ver_set = set(line.strip() for line in f if line.startswith("./%s" % path))
                vers.append(ver_set)
        except Exception as e:
            return str(e)
    files = sorted(list(vers[1] - vers[0]))
    return render_template('compare.html', files=files, ver1=ver1, ver2=ver2)

if __name__ == '__main__':
    app.run(debug=True)
