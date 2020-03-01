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
import re

import markdown
import logging
logging.captureWarnings(False)

from markdown import Extension
from markdown.extensions import toc 
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import ReferenceInlineProcessor, REFERENCE_RE
from markdown.inlinepatterns import AsteriskProcessor, EmStrongItem 
from markdown.inlinepatterns import EM_STRONG2_RE, STRONG_EM2_RE
from markdown.inlinepatterns import SMART_STRONG_EM_RE, SMART_STRONG_RE, SMART_EMPHASIS_RE

from urubu import UrubuWarning, urubu_warn, UrubuError, _warning, _error


def _set_dl_class(tree):
    for item in tree:
        if item.tag == 'dl':
            item.set('class', 'dl-horizontal')
        _set_dl_class(item)


class DLClass(Treeprocessor):

    def run(self, root):
        _set_dl_class(root)
        return None


class DLClassExtension(Extension):

    """Add 'dl-horizontal' class to definition list elements (for bootstrap)."""

    def extendMarkdown(self, md):
        md.treeprocessors.register(DLClass(md), 'dlclass', 3)


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

    def extendMarkdown(self, md):
        md.treeprocessors.register(TableClass(md), 'tableclass', 4)


class ProjectReferenceInlineProcessor(ReferenceInlineProcessor):

    def handleMatch(self, m, data):

        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        ref, end, shortref, handled = self.evalRef(data, index, text)
        if not handled:
            return None, None, None

        # Clean up linebreaks in ref
        ref = self.NEWLINE_CLEANUP_RE.sub(' ', ref)

        id = ref.lower()

        if id in self.md.references:
            href, title = self.md.references[id]
        else:
            anchor = None
            if '#' in ref:
                ref, anchor = ref.split('#', 1)
            this = self.md.this
            if not posixpath.isabs(ref):
                # treat empty ref as reference to current page
                if not ref: 
                    ref = this['components'][-1]
                rootrelpath = '/' + '/'.join(this['components'][:-1])
                id = posixpath.normpath(posixpath.join(rootrelpath, ref))
                id = id.lower()
            else:
                id = ref.lower()
            ref = ref.lower()
            if ref in self.md.site['reflinks']:
                if (ref != id) and (id in self.md.site['reflinks']):
                    raise UrubuError(_error.ambig_ref_md, msg=ref, fn=this['fn'])
                id = ref
            if id in self.md.site['reflinks']:
                item = self.md.site['reflinks'][id]
                href, title = item['url'], item['title']
                if shortref:
                    text = title
                    if anchor is not None:
                        text = anchor
                if anchor is not None:
                    anchor = toc.slugify(anchor, '-')
                    href = '%s#%s' % (href, anchor)
                    anchorref = '%s#%s' % (id, anchor)
                    self.md.this['_anchorrefs'].add(anchorref)

            else:  # ignore undefined refs
                urubu_warn(_warning.undef_ref_md, msg=ref, fn=this['fn'])
                return None, None, None

        return self.makeTag(href, title, text), m.start(0), end

    def evalRef(self, data, index, text):
        """
        Evaluate ref from [text][ref] or [ref][] 

        """
        shortref = False 
        m = self.RE_LINK.match(data, pos=index)
        if not m:
            return None, index, shortref, False 
        else:
            ref = m.group(1)
            end = m.end(0)
            if not ref:
                ref = text
        return ref, end, shortref, True 

class ProjectShortReferenceInlineProcessor(ProjectReferenceInlineProcessor):

    def evalRef(self, data, index, text):
        """
        Evaluate ref from [text]

        """
        shortref = True 
        return text, index, shortref, True 


class ProjectReferenceExtension(Extension):

    """Overwrite reference patterns with project reference extensions."""

    def extendMarkdown(self, md):
        md.inlinePatterns.deregister('reference')
        md.inlinePatterns.register(ProjectReferenceInlineProcessor(REFERENCE_RE, md), 'reference', 170)
        md.inlinePatterns.deregister('short_reference')
        md.inlinePatterns.register(ProjectShortReferenceInlineProcessor(REFERENCE_RE, md), 'short_reference', 130)


class ExtractAnchorsClass(Treeprocessor):

    def run(self, tree):
        this = self.md.this
        thisid = this['id']
        components = this['components']
        for item in tree:
            if 'id' in item.attrib:
                self.md.anchors.add("%s#%s" % (thisid, item.attrib['id']))
                # add special version for index files
                if components[-1] == 'index':
                    navid = thisid[:-6] # remove trailing backslash also
                    self.md.anchors.add("%s#%s" % (navid, item.attrib['id']))
        return None


class ExtractAnchorsExtension(Extension):

    def extendMarkdown(self, md):
        md.treeprocessors.register(ExtractAnchorsClass(md), 'extractanchors', 5)


# extension for the <mark> tag
class UnderscoreMarkProcessor(AsteriskProcessor):
    """Emphasis processor for handling strong and mark matches inside underscores."""

    PATTERNS = [
        EmStrongItem(re.compile(EM_STRONG2_RE, re.DOTALL | re.UNICODE), 'double', 'strong,mark'),
        EmStrongItem(re.compile(STRONG_EM2_RE, re.DOTALL | re.UNICODE), 'double', 'mark,strong'),
        EmStrongItem(re.compile(SMART_STRONG_EM_RE, re.DOTALL | re.UNICODE), 'double2', 'strong,mark'),
        EmStrongItem(re.compile(SMART_STRONG_RE, re.DOTALL | re.UNICODE), 'single', 'strong'),
        EmStrongItem(re.compile(SMART_EMPHASIS_RE, re.DOTALL | re.UNICODE), 'single', 'mark')
    ]

class MarkTagExtension(Extension):

    def extendMarkdown(self, md):
        md.inlinePatterns.deregister('em_strong2')
        md.inlinePatterns.register(UnderscoreMarkProcessor(r'_'), 'em_strong2', 50)



