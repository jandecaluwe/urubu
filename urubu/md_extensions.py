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

from warnings import warn
import posixpath

import markdown
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import ReferencePattern, REFERENCE_RE, SHORT_REF_RE

from urubu import UrubuWarning, UrubuError

undef_ref_warning = "Undefined ref [{}] in file '{}'"
ambig_ref_error = "Ambiguous ref [{}] in file '{}'"


def _set_table_class(tree):
    for item in tree:
        if item.tag == 'table':
            item.set('class', 'table')
        _set_table_class(item)

class TableClass(Treeprocessor):

    def run(self, root):
        _set_table_class(root)
        return None

class TableClassExtension(Extension):
    """Add 'table' class to table elements (for bootstrap)."""
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('tableclass', TableClass(md), "_end")

class ProjectReferencePattern(ReferencePattern):

    def handleMatch(self, m):
        try:
            ref = m.group(9).lower()
        except IndexError:
            ref = None
        shortref = False
        if not ref:
            # if we got something like "[Google][]" or "[Google]"
            # we'll use "google" as the id
            ref = m.group(2).lower()
            shortref = True

        text = m.group(2)
        # Clean up linebreaks in ref 
        ref = self.NEWLINE_CLEANUP_RE.sub(' ', ref)
        if ref in self.markdown.references:
            href, title = self.markdown.references[ref]
        else: 
            this = self.markdown.this
            if not posixpath.isabs(ref):
                rootrelpath = '/' +  '/'.join(this['components'][:-1])
                id = posixpath.normpath(posixpath.join(rootrelpath, ref))
                id = id.lower()
            else:
                id = ref
            if ref in self.markdown.site['reflinks']:
                if (ref != id) and (id in self.markdown.site['reflinks']):
                    raise UrubuError(ambig_ref_error.format(ref, this['fn']))  
                id = ref 
            if id in self.markdown.site['reflinks']:
                item = self.markdown.site['reflinks'][id]
                href, title = item['url'], item['title'] 
                if shortref:
                    text = title
            else: # ignore undefined refs
                warn(undef_ref_warning.format(ref, this['fn']), UrubuWarning)
                return None

        return self.makeTag(href, title, text)

class ProjectReferenceExtension(Extension):
    """Overwrite reference pattern with project reference extension."""
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['reference'] = ProjectReferencePattern(REFERENCE_RE, md)
        md.inlinePatterns['short_reference'] = ProjectReferencePattern(SHORT_REF_RE, md)
