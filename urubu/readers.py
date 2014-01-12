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
from io import open

import yaml
import re
import codecs
import warnings

from urubu import UrubuWarning

yamlfm_warning = 'No yaml frontmatter found in {}'

def get_yamlfm(fn):
    """Return the yaml frontmatter."""
    info = _get_yamlfm_helper(fn)
    if info is None:
        warnings.warn(yamlfm_warning.format(fn), UrubuWarning)
    return info

def _get_yamlfm_helper(fn):
    with open(fn, 'r', encoding='utf-8-sig') as f:
        line = f.readline()
        if line.strip() != '---':
            return None
        lines = []
        while True:
            line = f.readline()
            if not line:
                return None
            elif line.strip() == '---':
                s = '\n'.join(lines)
                meta = yaml.safe_load(s)
                if isinstance(meta, dict):
                    return meta
                else:
                    return None
            else:
               lines.append(line)

def get_yaml_navinfo(fn):
    """Read yaml navigation info."""
    with open(fn, 'r', encoding='utf-8-sig') as f:
        s = f.read()
        info = yaml.safe_load(s)
        return info
        
