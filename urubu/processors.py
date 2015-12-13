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
import os, json, itertools

import markdown
import logging
logging.captureWarnings(False)
from bs4 import BeautifulSoup

import jinja2

from urubu import UrubuWarning, UrubuError, urubu_warn, _warning
from urubu import md_extensions

from urubu.config import layoutdir, tag_layout, tipuesearchdir, tipuesearch_content
from urubu._compat import text_type

def skip_yamlfm(f):
    """Return source of a file without yaml frontmatter."""
    f.readline()
    found = False
    lines = []
    for line in f.readlines():
        if found:
            lines.append(line)
        if line.strip() == '---':
            found = True
    return ''.join(lines)


class ContentProcessor(object):

    def __init__(self, sitedir, project):
        self.sitedir = sitedir
        self.filelist = project.filelist
        self.navlist = project.navlist
        self.taglist = project.taglist
        self.site = project.site
        tableclass = md_extensions.TableClassExtension()
        projectref = md_extensions.ProjectReferenceExtension()
        extractanchors = md_extensions.ExtractAnchorsExtension()
        # there is a strange interaction between smarty and reference links that start on a new line
        # disabling smarty for now...
        # extensions = ['extra', 'codehilite', 'headerid', 'toc', 'smarty', tableclass, projectref]
        extensions = ['extra', 'codehilite', 'toc', 
                      tableclass, projectref, extractanchors]
        extension_configs = {'codehilite': [('guess_lang', 'False'),
                                            ('linenums', 'False')],
                             'toc': [('baselevel', 2)]
                             }
        self.md = markdown.Markdown(extensions=extensions,
                                    extension_configs=extension_configs)
        self.md.site = self.site
        self.md.anchors = project.anchors 
        env = self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(layoutdir),
                                            lstrip_blocks=True,
                                            trim_blocks=True
                                            )
        env.filters.update(project.filters)
        self.templates = {}
        for layout in project.layouts:
            self.templates[layout] = self.env.get_template(layout + '.html')
        # layout for tags is optional, triggers index file generation per tag
        try:
            self.templates[tag_layout] = self.env.get_template(
                tag_layout + '.html')
        except jinja2.exceptions.TemplateNotFound:
            if self.taglist:
                urubu_warn(_warning.undef_tag_layout, msg=tag_layout)

    def process(self):
        """Process the content.

        Conversion and rendering are done in separate phases, so
        that the full content is available to the rendering process.
        """
        self.convert()
        self.render()
        self.make_tipuesearch_content()

    def convert(self):
        for info in self.filelist:
            fn = info['fn']
            with open(fn, encoding='utf-8-sig') as inf:
                src = skip_yamlfm(inf)
            self.md.this = info
            self.md.toc = ''
            info['body'] = self.md.convert(src)
            info['toc'] = ''
            if hasattr(self.md, 'toc'):
                # filter out empty tocs, 35 is the magic length
                if len(self.md.toc) > 35:
                    info['toc'] = self.md.toc
            # markdown support in keys
            mdkeys = [key for key in info if key[-3:] == '.md']
            for mdkey in mdkeys:
                key = mdkey[:-3]
                info[key] = self.md.convert(info[mdkey])
            self.md.reset()
        for info in self.navlist:
            # markdown support in keys
            mdkeys = [key for key in info if key[-3:] == '.md']
            for mdkey in mdkeys:
                key = mdkey[:-3]
                info[key] = self.md.convert(info[mdkey])
            self.md.reset()

    def render(self):
        # content files
        for info in self.filelist:
            if info['layout'] is None:
                continue
            self.render_file(info)
        # tag index files
        if tag_layout not in self.templates:
            return
        for info in self.taglist:
            self.render_file(info)

    def render_file(self, info):
        layout = info['layout']
        templ = self.templates[layout]
        html = templ.render(this=info, site=self.site)
        # extract text from html for search support
        self.extract_text(html, info)
        fn = info['fn']
        bfn, ext = os.path.splitext(fn)
        outfn = os.path.join(self.sitedir, bfn) + self.site['file_ext']
        with open(outfn, 'w', encoding='utf-8', errors='strict') as outf:
            outf.write(html)

    def extract_text(self, html, info):
        # select main tag for search content
        m = BeautifulSoup(html, "html.parser").select('main')
        text = ""
        if m:
            text = m[0].get_text(" ", strip=True)
        info['text'] = text

    def make_tipuesearch_content(self):
        tsd = os.path.join(self.sitedir, tipuesearchdir)
        if not os.path.isdir(tsd):
            return
        tsc = os.path.join(tsd, tipuesearch_content)
        items = [] 
        # use tag index files if they have been rendered
        taglist = []
        if tag_layout in self.templates:
           taglist = self.taglist
        for info in itertools.chain(self.filelist, taglist):
            if 'text' not in info:
                return
            tags = ""
            if 'tags' in info:
               tags = ' '.join(info['tags'])
            item = {'text' : info['text'],
                    'title': info['title'],
                    'url'  : info['url'],
                    'tags' : tags} 
            items.append(item)
        obj = {'pages': items}
        with open(tsc, 'w', encoding='utf-8') as fd:
            # json.dump is buggy in Python2 -- use workaround
            # print json.dumps(obj, ensure_ascii=False, indent=4) 
            data = json.dumps(obj, fd, ensure_ascii=False, indent=4, sort_keys=True) 
            fd.write(text_type(data))


