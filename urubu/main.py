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
from sys import stderr

from urubu import __version__
from urubu import project

from urubu._compat import socketserver, httpserver
from urubu.httphandler import AliasingHTTPRequestHandler

__IDESC__ = """
Micro CMS tool to build and test static websites.
"""

__IEPILOG__ = """
Documentation: <https://urubu.jandecaluwe.com/manual/>
"""

def serve(baseurl, host='localhost', port=8000):
    """HTTP server straight from the docs."""
    # allow running this from the top level
    if os.path.isdir('_build'):
        os.chdir('_build')
    # local use, address reuse should be OK
    socketserver.TCPServer.allow_reuse_address = True
    handler = AliasingHTTPRequestHandler
    httpd = socketserver.TCPServer((host, port), handler)
    httpd.baseurl = baseurl

    if host == '':
        print("This web server is not safe for public/production use.", file=stderr)
        print("Serving all peers at port {port}...\n\
Browse <http://localhost:{port}/> (*:{port})".format(host=host, port=port))
    else:
        print("Serving {host} at port {port}...\n\
Browse <http://{host}:{port}/>.".format(host=host, port=port))
    if httpd.baseurl: print("Using baseurl {}".format(httpd.baseurl))
    httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser(prog='python -m urubu', add_help=False,
                                     epilog=__IEPILOG__, description=__IDESC__)
    parser.add_argument('-h', '--help', action='help', help="show program's help and exit")
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('command', choices=['build', 'serve', 'serveany'])
    args = parser.parse_args()
    if args.command == 'build':
        project.build()
    elif args.command == 'serve':
        proj = project.load()
        serve(proj.site['baseurl'])
    elif args.command == 'serveany':
        proj = project.load()
        serve(proj.site['baseurl'], host='')
