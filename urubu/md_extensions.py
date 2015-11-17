# Copyright 2014-2015 Jan Decaluwe
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

import posixpath

import markdown
import logging
logging.captureWarnings(False)

from markdown import Extension
from markdown.extensions import toc 
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import ReferencePattern, REFERENCE_RE, SHORT_REF_RE

from urubu import UrubuWarning, urubu_warn, UrubuError, _warning, _error

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
            ref = m.group(9)
        except IndexError:
            ref = None
        shortref = False
        if not ref:
            # if we got something like "[Google][]" or "[Google]"
            # we'll use "google" as the id
            ref = m.group(2)
            shortref = True

        # Clean up linebreaks in ref
        ref = self.NEWLINE_CLEANUP_RE.sub(' ', ref)

        text = m.group(2)
        id = ref.lower()

        if id in self.markdown.references:
            href, title = self.markdown.references[id]
        else:
            anchor = None
            if '#' in ref:
                ref, anchor = ref.split('#', 1)
            this = self.markdown.this
            if not posixpath.isabs(ref):
                rootrelpath = '/' + '/'.join(this['components'][:-1])
                id = posixpath.normpath(posixpath.join(rootrelpath, ref))
                id = id.lower()
            else:
                id = ref.lower()
            ref = ref.lower()
            if ref in self.markdown.site['reflinks']:
                if (ref != id) and (id in self.markdown.site['reflinks']):
                    raise UrubuError(_error.ambig_ref_md, msg=ref, fn=this['fn'])
                id = ref
            if id in self.markdown.site['reflinks']:
                item = self.markdown.site['reflinks'][id]
                href, title = item['url'], item['title']
                if shortref:
                    text = title
                    if anchor is not None:
                        text = anchor
                if anchor is not None:
                    anchor = toc.slugify(anchor, '-')
                    href = '%s#%s' % (href, anchor)
                    anchorref = '%s#%s' % (id, anchor)
                    self.markdown.this['_anchorrefs'].add(anchorref)
            else:  # ignore undefined refs
                urubu_warn(_warning.undef_ref_md, msg=ref, fn=this['fn'])
                return None

        return self.makeTag(href, title, text)


class ProjectReferenceExtension(Extension):

    """Overwrite reference pattern with project reference extension."""

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['reference'] = ProjectReferencePattern(
            REFERENCE_RE, md)
        md.inlinePatterns['short_reference'] = ProjectReferencePattern(
            SHORT_REF_RE, md)


class ExtractAnchorsClass(Treeprocessor):

    def run(self, tree):
        this = self.markdown.this
        thisid = this['id']
        components = this['components']
        for item in tree:
            if 'id' in item.attrib:
                self.markdown.anchors.add("%s#%s" % (thisid, item.attrib['id']))
                # add special version for index files
                if components[-1] == 'index':
                    navid = thisid[:-6] # remove trailing backslash also
                    self.markdown.anchors.add("%s#%s" % (navid, item.attrib['id']))
        return None


class ExtractAnchorsExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('extractanchors', ExtractAnchorsClass(md), "_end")


