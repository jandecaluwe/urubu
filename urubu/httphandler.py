# Copyright 2015 Sreepathi Pai
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

from urubu._compat import httpserver

class AliasingHTTPRequestHandler(httpserver.SimpleHTTPRequestHandler):
    def do_GET(self):
        baseurl = self.server.baseurl

        if not baseurl:
            httpserver.SimpleHTTPRequestHandler.do_GET(self)
            return

        wk_baseurl = "/%s/" % (baseurl)

        if self.path == wk_baseurl[:-1]:
            # handle /$baseurl -> /$baseurl/

            self.send_response(301, 'Moved Permanently')
            self.send_header('Location', wk_baseurl)
            self.end_headers()
            return

        if self.path[:len(wk_baseurl)] == wk_baseurl:
            # translate /$baseurl/path internally to /path and serve

            self.path = self.path[len(wk_baseurl)-1:]
            httpserver.SimpleHTTPRequestHandler.do_GET(self)
            return
        else:
            # handle /xyz/path -> /$baseurl/xyz/path
            #
            # usually caused by underlying server sending a redirect
            # to non-baseurl-prefixed path

            self.send_response(302, 'Moved Temporarily')
            sep = "/" if self.path[0] != "/" else ""

            # note this replicates underlying bugs in that Location is
            # not absolute as required by the spec and we throw away
            # '?' and '#'

            self.send_header('Location', "/%s%s%s" % (baseurl, sep, self.path))
            self.end_headers()
            return
