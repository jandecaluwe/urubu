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

# Python 3 idioms
from __future__ import unicode_literals

import os

configfn = '_config.yml'
siteinfofn = '_site.yml'
sitedir = '_build'
tagdir = 'tag'
tagid = '/' + tagdir
tagindexid = tagid + '/' + 'index'
tag_layout = 'tag'
layoutdir = '_layouts'
tipuesearchdir = 'tipuesearch'
tipuesearch_content = 'tipuesearch_content.json'
