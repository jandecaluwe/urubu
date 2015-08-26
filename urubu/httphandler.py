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

        if self.path == "/":
            # for convenience
            self.send_response(302, 'Moved Temporarily')
            self.send_header('Location', "/%s/" % (baseurl,))
            self.end_headers()
            return
        else:
            wk_baseurl = "/%s/" % (baseurl)
            if self.path[:len(wk_baseurl)] == wk_baseurl:
                self.path = self.path[len(wk_baseurl)-1:]
                httpserver.SimpleHTTPRequestHandler.do_GET(self)
            elif self.path == wk_baseurl[:-1]:
                self.send_response(301, 'Moved Permanently')
                self.send_header('Location', "/%s/" % (baseurl,))
                self.end_headers()
                return        
