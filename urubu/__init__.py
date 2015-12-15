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

__version__ = "0.9.0"

from warnings import warn

class UrubuWarning(UserWarning):
    pass

def urubu_warn(kind, msg='', fn=''):
    if fn:
        fn = 'in ' + fn + ': '
    if msg:
        msg = ': ' + "'{}'".format(msg)
    warn(fn + kind + msg, UrubuWarning, stacklevel=2)


class UrubuError(Exception):
    def __init__(self, kind, msg='', fn=''):
        self.kind = kind
        self.msg = msg
        self.fn = fn 
    def __str__(self):
        fn = self.fn 
        if fn:
            fn = 'in ' + fn + ': '
        msg = self.msg
        if msg:
            msg = ': ' + "'{}'".format(msg)
        return fn + self.kind + msg

class _error():
    pass

class _warning():
    pass

_warning.no_yamlfm = "No yaml front matter - ignored"
_warning.undef_tag_layout = "Tags defined, but no tag layout found"
_warning.undef_ref_md = 'Undefined reference'
_warning.undef_anchor = "Undefined anchor"

_error.ambig_refid = "Ambiguous reference id"
_error.undef_ref = "Undefined reference"
_error.ambig_ref = "Ambiguous reference, cannot resolve"
_error.undef_info = "Missing attribute"
_error.date_format = "Date format error - should be YYYY-MM-DD"
_error.undef_key = "Undefined key"
_error.undef_content = "No 'content' or 'order' specified"
_error.undef_reflink_key = "Undefined key in site reflink"
_error.ambig_ref_md = 'Ambiguous reference' 
