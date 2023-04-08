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
import os, sys, json, itertools

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
        dlclass = md_extensions.DLClassExtension()
        tableclass = md_extensions.TableClassExtension()
        projectref = md_extensions.ProjectReferenceExtension()
        extractanchors = md_extensions.ExtractAnchorsExtension()
        marktag = md_extensions.MarkTagExtension()
        # there is a strange interaction between smarty and reference links that start on a new line
        # disabling smarty for now...
        # extensions = ['extra', 'codehilite', 'headerid', 'toc', 'smarty', tableclass, projectref]
        extensions = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc',
                      dlclass, tableclass, projectref, extractanchors]
        if self.site['mark_tag_support']:
            extensions.append(marktag)
        extension_configs = {'markdown.extensions.codehilite': [('guess_lang', 'False'),
                                                                ('linenums', 'False')],
                             'markdown.extensions.toc': [('baselevel', 2)]
                             }
        self.md = markdown.Markdown(extensions=extensions,
                                    extension_configs=extension_configs)
        self.md.site = self.site
        self.md.anchors = project.anchors
        if 'strict_undefined' in self.site and self.site['strict_undefined']:
            undefined_class = jinja2.StrictUndefined
        else:
            undefined_class = jinja2.Undefined
        env = self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(layoutdir),
            lstrip_blocks=True,
            trim_blocks=True,
            undefined=undefined_class)
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
        self.pagination()
        self.render()
        self.make_tipuesearch_content()

    def pagination(self):
        # We look at attributes in pages here, e.g.:
        #
        #   items_per_page: 5
        #   items_index: news\index.md
        #
        #   OR
        #
        #   items_per_page: 5
        #   items_filter: mysteries time-loop
        #
        # We then find the info item for the items index/filter and
        # use it to create more entries for the current item in
        # the file list, splitting it out into items_per_page
        # chunks for each file.
        #  
        # The filters are the same ones defined in _python for Jinja2
        # to use.  The name of the function is followed by its parameters
        #
        # The page and any new pages created from it will get new attributes:
        #
        #     numpages - the number of total pages generated
        #     thispage - the page number of this page in the chain
        #     prevpage - the previous page in the chain
        #     nextpage - the next page in the chain
        #     pages    - a list of page numbers and page objects
        # 
        # The first page will have no prevpage, and the last page
        # will have no nextpage.

        import math
        
        for info in self.filelist:
            source = None
            
            if 'items_per_page' in info:
                if 'items_index' in info:
                    if info['items_index'] == "this":
                        source = info['content']
                    else:
                        source = next(x for x in self.filelist if x['fn'] == info['items_index'])['content']
            
                if 'items_filter' in info:
                    filter = info['items_filter'].split()
                    source = self.env.filters[filter[0]](*filter[1:])
                
                if source:
                    items_per_page = info['items_per_page']
                    
                    # This will be a shared list among all the pages
                    # that lists each page along with its page number,
                    # e.g. {'pagenum': 1, 'page': info}
                    pages = []
                    
                    # Split source into items_per_page sized chunks,
                    # starting with info and then creating new
                    # files with incrementing numbers
                    
                    chunks = math.ceil(len(source) / items_per_page)

                    # First chunk is always the current page
                    info['content'] = source[0:items_per_page]
                    
                    # See if we even need to worry about pagination
                    # Maybe everything fits on the one page already
                    if len(source) <= items_per_page:
                        continue
                    
                    info['numpages'] = chunks
                    info['thispage'] = 1
                    info['pages'] = pages
                    
                    pages.append({'pagenum': 1, 'page': info})
                    
                    chunk = 1
                    prev_page = info
                    
                    # If we need more chunks, split off new pages for them
                    while chunk < chunks:
                        chunk += 1
                        new_info = info.copy()
                        # Prevent the new page from spinning off new pages
                        del new_info['items_per_page']
                        
                        new_info['pages'] = pages
                        pages.append({'pagenum': chunk, 'page': new_info})
                        
                        # Set the content to the right slice of the source
                        new_info['content'] = source[(chunk-1)*items_per_page:(chunk-1)*items_per_page+items_per_page]
                        
                        new_info['numpages'] = chunks
                        new_info['thispage'] = chunk

                        # Name the new page based on its chunk number
                        fn_parts = os.path.splitext(new_info['fn'])
                        new_info['fn'] = fn_parts[0]+str(chunk)+fn_parts[1]

                        fn_parts = os.path.splitext(new_info['url'])
                        new_info['url'] = fn_parts[0]+str(chunk)+fn_parts[1]
                        
                        # Setup the prevpage and nextpage attributes
                        new_info['prevpage'] = prev_page
                        prev_page['nextpage'] = new_info
                        # We may have inherited this from the first chunk
                        if 'nextpage' in new_info:
                            del new_info['nextpage']
                        
                        prev_page = new_info
                        
                        self.filelist.append(new_info)
        
    def convert(self):
        for info in self.filelist:
            fn = info['fn']
            with open(fn, encoding='utf-8-sig') as inf:
                src = skip_yamlfm(inf)
            self.md.this = info
            # first process as a template
            try:
                templ = self.env.from_string(src)
                src = templ.render(this=info, site=self.site)
            except:
                exc, msg, tb = sys.exc_info()
                raise UrubuError(str(exc), msg=msg, fn=fn)
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

        # check if filename is overriden
        if info.get('saveas') is not None:
            outfn = os.path.join(self.sitedir, info.get('saveas'))
        else:
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
                continue
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
            data = json.dumps(obj, ensure_ascii=False, indent=4, sort_keys=True)
            fd.write(text_type(data))
