# Copyright 2014 Jan Decaluwe
#
# This file is part of Urubu.
#
# Urubu is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Urubu is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Urubu.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import argparse

import os

from urubu import __version__
from urubu import project

from urubu._compat import socketserver, httpserver
from urubu.httphandler import AliasingHTTPRequestHandler

def serve(project):
    """HTTP server straight from the docs."""
    # allow running this from the top level
    if os.path.isdir('_build'):
        os.chdir('_build')
    # local use, address reuse should be OK
    socketserver.TCPServer.allow_reuse_address = True
    PORT = 8000
    handler = AliasingHTTPRequestHandler
    httpd = socketserver.TCPServer(('', PORT), handler)
    httpd.baseurl = project.site['baseurl']
        
    print("Serving at port {}".format(PORT))
    if httpd.baseurl: print("Using baseurl {}".format(httpd.baseurl))
    httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser(prog='python -m urubu')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('command', choices=['build', 'serve'])
    args = parser.parse_args()
    if args.command == 'build':
        project.build()
    elif args.command == 'serve':
        proj = project.load()
        serve(proj)
