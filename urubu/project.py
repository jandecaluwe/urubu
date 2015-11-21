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

import os
import yaml
import fnmatch
import shutil
import datetime
import itertools
from operator import itemgetter

from urubu._compat import ifilter

from urubu import UrubuWarning, UrubuError, urubu_warn, _warning, _error
from urubu import readers, processors

from urubu.config import (configfn, siteinfofn, sitedir,
                          tagdir, tagid, tagindexid, tag_layout)

def require_key(key, mapping, tipe, fn):
    type_error = "{}: '{}' value should be of type {}"
    if key in mapping:
        if not (isinstance(mapping[key], tipe)):
            raise TypeError(type_error.format(fn, key, tipe))


def get_relpath(path, start):
    return os.path.relpath(path, start)


def get_components(path, hasext=True):
    p = path
    if hasext:
        p, ext = os.path.splitext(path)
    p = p.lstrip(os.curdir)
    p = p.strip(os.sep)
    components = []
    if p:
        components = p.split(os.sep)
    return components

def make_id(components, lowercased=True):
    id = ('/' + '/'.join(components))
    if lowercased:
        return id.lower()
    return id


def make_clean(dir):
    for fn in os.listdir(dir):
        p = os.path.join(sitedir, fn)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.isfile(p):
            os.remove(p)


class Project(object):

    def __init__(self):
        self.cwd = os.getcwd()
        self.config = {}
        self.site = {'brand': '',
                     'baseurl': None,
                     'reflinks': {},
                     'link_ext': '.html',
                     'file_ext': '.html'
                     }
        self.filelist = []
        self.navlist = []
        self.taglist = []
        self.tagmap = {}
        self.filters = {}
        self.validators = {}
        self.layouts = []
        # anchors to be filled in by markdown processor
        self.anchors = set()


    def get_config(self):
        """Get the config data from the yaml config file."""
        if os.path.isfile(configfn):
            with open(configfn, encoding='utf-8-sig') as f:
                self.config = yaml.safe_load(f)

    def get_siteinfo(self):
        """Get the siteinfo from the yaml data file."""
        if not os.path.isfile(siteinfofn):
            return
        with open(siteinfofn, encoding='utf-8-sig') as f:
            meta = yaml.safe_load(f)
        # validate the site reflinks and add them
        if 'reflinks' in meta:
            for id in meta['reflinks']:
                info = meta['reflinks'][id]
                self.validate_sitereflink(id, info)
                self.add_reflink(id, info)
            del meta['reflinks']
        self.site.update(meta)

    def get_pythonhooks(self):
        """Get user-defined python hooks."""
        # add cwd to path to make it entry points work on windows
        import sys
        sys.path.insert(0, os.getcwd())
        try:
            import _python
        except ImportError:
            _python = None
        if _python is not None:
            if hasattr(_python, 'filters'):
                self.filters = _python.filters
            if hasattr(_python, 'validators'):
                self.validators = _python.validators

    def validate_sitereflink(self, id, info):
        if 'title' not in info:
            raise UrubuError(_error.undef_reflink_key, fn=id, msg=id + ': title')
        if 'url' not in info:
            raise UrubuError(_error.undef_reflink_key, fn='_site.yml', msg=id + ': url')

    def add_reflink(self, id, info):
        """Add a valid reflink to the site reflinks."""
        id = id.lower()
        if id in self.site['reflinks']:
            raise UrubuError(_error.ambig_refid, msg=id)
        self.site['reflinks'][id] = info

    def finalize_local_url(self, url):
        """Add a base to a local URL, if configured."""
        if self.site['baseurl']:
            url = '/' + self.site['baseurl'] + url
        return url

    def get_contentinfo(self):
        """Get info from the markdown content files."""
        pattern = '*.md'
        ignore_patterns = self.get_ignore_patterns()
        for path, dirnames, filenames in os.walk(self.cwd):
            relpath = get_relpath(path, self.cwd)
            if any(fnmatch.fnmatch(relpath, ip) for ip in ignore_patterns):
                continue

            for fn in filenames:
                if fnmatch.fnmatch(fn, pattern):
                    # normalize to convert ./foo into foo
                    # to avoid problems with ignore_patterns matching
                    relfn = os.path.normpath(os.path.join(relpath, fn))
                    if any(fnmatch.fnmatch(relfn, ip) for ip in ignore_patterns):
                        continue
                    meta = readers.get_yamlfm(relfn)
                    if meta is None:
                        urubu_warn(_warning.no_yamlfm, fn=relfn)
                        continue
                    fileinfo = self.make_fileinfo(relfn, meta)
                    self.filelist.append(fileinfo)
                    # validate after file info has been added so it can be used
                    self.validate_fileinfo(relfn, fileinfo)
                    self.add_reflink(fileinfo['id'], fileinfo)
                    if fn == 'index.md':
                        # start from fileinfo of index file
                        navinfo = self.make_navinfo(relpath, fileinfo)
                        self.navlist.append(navinfo)
                        self.validate_navinfo(relfn, navinfo)
                        self.add_reflink(navinfo['id'], navinfo)
                        # add nav info to tag map
                        self.add_info_to_tagmap(navinfo)
                    else:
                        # add id for non-index files to tag tags
                        self.add_info_to_tagmap(fileinfo)

    def validate_fileinfo(self, relfn, info):
        # layout is mandatory
        if 'layout' not in info:
            raise UrubuError(_error.undef_info, msg='layout', fn=relfn)
        if 'layout' is None:
            return
        layout = info['layout']
        # modification date, always available
        t = os.path.getmtime(relfn)
        info['mdate'] = datetime.date.fromtimestamp(t)
        # first run a validator if it exist
        if layout in self.validators:
            self.validators[layout](info)
        # a validator may add/modify attributes
        layout = info['layout']
        if layout is None:
            return
        if layout not in self.layouts:
            self.layouts.append(layout)
        # title
        if 'title' not in info:
            raise UrubuError(_error.undef_info, msg='title', fn=relfn)
        # date
        if 'date' in info:
            if not isinstance(info['date'], datetime.date):
               raise UrubuError(_error.date_format, fn=relfn)
        # tags
        if 'tags' in info:
            # TODO: make sure it's a list of strings
            if isinstance(info['tags'], str):
                info['tags'] = [info['tags']]
            # TODO: normalize tags

    def validate_navinfo(self, relfn, info):
        if ('content' not in info) and ('order' not in info):
            # exception: tag folder doesn't require content atribute
            # set it to empty list align with normal folders
            if info['id'] == tagid:
                info['content'] = []
            else:
                raise UrubuError(_error.undef_content, fn=relfn)
        require_key('content', info, list, relfn)

    def make_fileinfo(self, relfn, meta):
        """Make a fileinfo dict."""
        info = {}
        info['fn'] = relfn
        info['components'] = components = get_components(relfn)
        info['id'] = make_id(components)
        # make html url from ref
        info['url'] = self.finalize_local_url(
            make_id(components, lowercased=False) + self.site['link_ext'])
        info['_anchorrefs'] = set()
        info.update(meta)
        return info

    def make_navinfo(self, relpath, fileinfo):
        """Make a navinfo dict."""
        # start from fileinfo of index file
        info = fileinfo.copy()
        # overwrite attributes according to navinfo view
        info['fn'] = relpath
        info['components'] = components = get_components(relpath)
        info['id'] = make_id(components)
        # add trailing slash for navigation url
        info['url'] = self.finalize_local_url(info['id'])
        if info['url'] != '/':
            info['url'] += '/'
        return info

    def add_info_to_tagmap(self, info):
        """Add id to tagmap."""
        # tags are optional
        if 'tags' not in info:
            return
        for tag in info['tags']:
            if tag not in self.tagmap:
                self.tagmap[tag] = []
            self.tagmap[tag].append(info)

    def resolve_reflinks(self):
        for info in self.navlist:
            if 'content' in info:
                self.resolve_content(info)
            else:  # order
                assert 'order' in info
                self.get_content(info)
            # make reflinks content available in index file also
            index_id = make_id(info['components'] + ['index'])
            self.site['reflinks'][index_id]['content'] = info['content']

    def resolve_content(self, info):
        """Resolve reflinks in a folder."""
        refcontent = []
        for item in info['content']:
            if isinstance(item, dict):
                link = self.resolve_linkspec(item, info)
            else:
                link = self.resolve_ref(item, info)
            refcontent.append(link)
        # overwrite content ids with resolved refs
        info['content'] = refcontent

    def resolve_ref(self, ref, info):
        """Resolve a reference."""
        reflinks = self.site['reflinks']
        ref = ref.lower()
        path = os.path.normpath(os.path.join(info['fn'], ref))
        indexfn = info['fn'] + '/index'
        id = make_id(get_components(path, hasext=False))
        if ref in reflinks:
            if (ref != id) and (id in reflinks):
                raise UrubuError(_error.ambig_ref, msg=ref, fn=indexfn)
            id = ref
        elif not id in reflinks:
            raise UrubuError(_error.undef_ref, msg=ref, fn=indexfn)
        return reflinks[id]

    def resolve_linkspec(self, linkspec, info):
        link = {}
        link['url'] = link['title'] = linkspec.get('url', None)
        if 'ref' in linkspec:
            reflink = self.resolve_ref(linkspec['ref'], info)
            link.update(reflink)
        if 'title' in linkspec:
            link['title'] = linkspec['title']
        return link

    def get_content(self, info):
        """Infer sorted content of a folder."""
        reflinks = self.site['reflinks']
        refcontent = []
        key = info['order']
        reverse = info.get('reverse', False)
        navcomps = info['components']

        def pred(item):
            itemcomps = item['components']
            if len(itemcomps) == len(navcomps) + 1 and \
               itemcomps[:-1] == navcomps and \
               itemcomps[-1] != 'index' and \
               item['layout'] is not None:
                if key not in item:
                    raise UrubuError(_error.undef_key, msg=key, fn=item['fn'])
                return True
            return False
        allinfo = itertools.chain(self.filelist, self.navlist)
        refcontent = ifilter(pred, allinfo)

        def get_keyval(item):
            return item[key]
        refcontent = sorted(refcontent, key=get_keyval, reverse=reverse)
        info['content'] = refcontent

    def make_breadcrumbs(self):
        for info in self.filelist:
            breadcrumbs = []
            id = ''
            comps = info['components']
            # discard index
            if comps[-1] == 'index':
                comps = comps[:-1]
            for comp in comps:
                id = id + '/' + comp
                id = id.lower()
                breadcrumbs.append(self.site['reflinks'][id])
            info['breadcrumbs'] = breadcrumbs

    def make_pager(self):
        for info in self.navlist:
            content = info['content']
            if not content:
                return
            content[0]['prev'] = None
            for i in range(1, len(content)):
                content[i - 1]['next'] = content[i]
                content[i]['prev'] = content[i - 1]
            content[-1]['next'] = None

    def make_taginfo(self, tag, content):
        """Make a taginfo dict."""
        info = {}
        info['title'] = info['tag'] = tag
        info['layout'] = tag_layout
        info['fn'] = os.path.join(tagdir, tag, 'index')
        info['components'] = components = (tagdir, tag)
        info['id'] = make_id(components)
        # add trailing slash for tag index url
        info['url'] = self.finalize_local_url(info['id']) + '/'
        info['content'] = content
        return info

    def process_tags(self):
        """ Process tag map and tag content."""
        def get_date(item):
            """ Return item's date, or mdate as fallback."""
            if 'date' in item:
                return item['date']
            else:
                return item['mdate']
        for tag in self.tagmap.keys():
            # sort tag content by date
            content = sorted(self.tagmap[tag], key=get_date, reverse=True)
            taginfo = self.make_taginfo(tag, content)
            self.taglist.append(taginfo)
            self.add_reflink(taginfo['id'], taginfo)

        # sort tags according to content length, then alphabetically
        # to get sort order right, invert content length
        def get_tagkey(taginfo):
            return (-len(taginfo['content']), taginfo['tag'])
        self.taglist = sorted(self.taglist, key=get_tagkey)

        # set up tagid info dict if it doesn't exist already
        if tagid not in self.site['reflinks']:
            self.site['reflinks'][tagid] = {}
        self.site['reflinks'][tagid]['content'] = self.taglist
        # propagate content to index file if it exists
        if tagindexid in self.site['reflinks']:
            self.site['reflinks'][tagindexid]['content'] = self.taglist

    def get_ignore_patterns(self):
        ignore_patterns = ('.?*', '_*', 'Makefile')
        if 'ignore_patterns' in self.site:
            ignore_patterns += tuple(self.site['ignore_patterns'])
        return ignore_patterns

    def check_anchor_links(self):
        for info in self.filelist:
            for ar in info['_anchorrefs']:
                if not ar in self.anchors:
                    urubu_warn(_warning.undef_anchor, msg=ar, fn=info['id'] ) 

    def make_site(self):
        """Make the site."""
        # Keep sitedir alive if it exists, for the server
        if not os.path.exists(sitedir):
            os.mkdir(sitedir)
        make_clean(sitedir)
        ignore_patterns = self.get_ignore_patterns() + ('*.md',)
        ignore = shutil.ignore_patterns(*ignore_patterns)
        for fn in os.listdir(self.cwd):
            if any(fnmatch.fnmatch(fn, ip) for ip in ignore_patterns):
                continue
            wp = os.path.join(self.cwd, fn)
            sp = os.path.join(sitedir, fn)
            if os.path.isdir(wp):
                shutil.copytree(wp, sp, ignore=ignore)
            elif os.path.isfile(wp):
                shutil.copyfile(wp, sp)
        # make tag index dirs
        if self.taglist:
            tagpath = os.path.join(sitedir, tagdir)
            if not os.path.isdir(tagpath):
                os.mkdir(tagpath)
            for taginfo in self.taglist:
                os.mkdir(os.path.join(tagpath, taginfo['tag']))
        self.process_content()
        self.check_anchor_links()

    def process_content(self):
        """Process the content files."""
        p = processors.ContentProcessor(sitedir, project=self)
        p.process()

# import pprint

def load():
    proj = Project()
    proj.get_config()
    proj.get_siteinfo()
    return proj

def build():
    proj = load()
    proj.get_pythonhooks()
    proj.get_contentinfo()
    proj.resolve_reflinks()
    # pprint.pprint(proj.site['reflinks'])
    proj.make_breadcrumbs()
    proj.make_pager()
    proj.process_tags()
    proj.make_site()
