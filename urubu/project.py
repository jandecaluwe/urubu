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
from warnings import warn
import shutil
import datetime
import itertools

from urubu import UrubuWarning, UrubuError
from urubu import readers, processors 

configfn = '_config.yml'
siteinfofn = '_site.yml'
workdir = os.getcwd()
sitedir = '_build'

yamlfm_warning = "No yaml front matter in '{}' - ignored"
undef_ref_error = "Undefined reference '{}' in '{}'"
ambig_ref_error = "Ambiguous reference id '{}'"
undef_layout_error = "'layout' undefined in {}"
undef_meta_error = "{} '{}' has no '{}' attribute"
date_error = "Date format error in '{}' (should be YYYY-MM-DD)"
undef_key_error = "Undefined key '{}' in '{}'"
undef_content_error = "No 'content' or 'order' specified in {}"

type_error = "'{}' value should be a '{}' in '{}'"  

def require(key, mapping, tipe, fn):
    if key in mapping:
        if not (isinstance(mapping[key], tipe)):
            raise TypeError(type_error.format(key, tipe, fn))

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

def make_id(components):
    return ('/' + '/'.join(components)).lower()

def make_clean(dir):
    for fn in os.listdir(dir):
        p = os.path.join(sitedir, fn)
        if os.path.isdir(p):
            shutil.rmtree(p) 
        elif os.path.isfile(p):
            os.remove(p)

class Project(object):

    def __init__(self):
        self.config = {}
        self.site = {'brand' : '',
                     'reflinks': {}
                    }
        self.fileinfo = []
        self.filerefs = {}
        self.navinfo = [] 
	self.navrefs = {}
        self.filters = {}
        self.validators = {}
        self.layouts = []

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
            raise UrubuError(undef_meta_error.format('Site reflink', id, 'title'))
        if 'url' not in info:
            raise UrubuError(undef_meta_error.format('Site reflink', id, 'url'))

    def add_reflink(self, id, info):
        """Add a valid reflink to the site reflinks."""
        id = id.lower()
        if id in self.site['reflinks']:
            raise UrubuError(ambig_ref_error.format(id))
        self.site['reflinks'][id] = info 
         
    def get_contentinfo(self):
        """Get info form the markdown content files."""
        pattern = '*.md'
        for path, dirnames, filenames in os.walk(workdir):
            relpath = get_relpath(path, workdir)
            for fn in filenames:
                if fnmatch.fnmatch(fn, pattern):
                    relfn = os.path.join(relpath, fn) 
                    meta = readers.get_yamlfm(relfn)
                    if meta is None:
                        warn(yamlfm_warning.format(relfn), UrubuWarning)
                        continue
                    info = self.make_fileinfo(relfn, meta)
                    self.fileinfo.append(info)
                    # validate after file info has been added so it can be used
                    self.validate_filemeta(relfn, info)
                    self.add_reflink(info['id'], info)
                    if fn == 'index.md':
                        info = self.make_navinfo(relpath, meta)
                        self.navinfo.append(info)
                        self.validate_navmeta(relfn, info)
                        self.add_reflink(info['id'], info)

    def validate_filemeta(self, relfn, meta):
        if 'layout' not in meta:
            raise UrubuError(undef_meta_error.format('File', relfn, 'layout'))
        layout = meta['layout']
        # first run a validator if it exist
        if layout in self.validators:
            self.validators[layout](meta)
        # a validator may add/modify attributes
        layout = meta['layout']
        if layout is None:
            return
        if layout not in self.layouts:
            self.layouts.append(layout)
        if 'title' not in meta:
            raise UrubuError(undef_meta_error.format('File', relfn, 'title'))
        if 'date' in meta:
            if not isinstance(meta['date'], datetime.date):
                raise UrubuError(date_error.format(relfn))

    def validate_navmeta(self, relfn, meta):
        if ('content' not in meta) and ('order' not in meta):
            raise UrubuError(undef_content_error.format(relfn))
        require('content', meta, list, relfn)

    def make_fileinfo(self, relfn, meta):
        """Make a fileinfo dict."""
        info = {}
        info['fn'] = relfn 
        info['components'] = components = get_components(relfn)
        info['id'] = make_id(components)
        # make html url from ref 
        info['url'] = info['id'] + '.html'
        info.update(meta)
        return info

    def make_navinfo(self, relpath, meta):
        """Make a navinfo dict."""
        info = {}
        info['fn'] = relpath 
        info['components'] = components = get_components(relpath)
        info['id'] = make_id(components)
        # add trailing slash for navigation url
        info['url'] = info['id']
        if info['url'] != '/':
            info['url'] += '/'
        info.update(meta)
        return info

    def resolve_reflinks(self):
        for info in self.navinfo:
            if 'content' in info:
                self.resolve_content(info)
            else: # order
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
        if ref in reflinks:
           id = ref    
        else:
           path = os.path.normpath(os.path.join(info['fn'], ref)) 
           id = make_id(get_components(path, hasext=False)) 
           if not id in reflinks:
               raise UrubuError(undef_ref_error.format(ref, info['fn']))  
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
            if len(itemcomps) == len(navcomps)+1 and \
               itemcomps[:-1] == navcomps and \
               itemcomps[-1] != 'index' and \
               item['layout'] is not None:
               if key not in item:
                   raise UrubuError(undef_key_error.format(key, item['fn'])) 
               return True
            return False 
        allinfo = itertools.chain(self.fileinfo, self.navinfo)
        refcontent = itertools.ifilter(pred, allinfo)

        def get_keyval(item):
            return item[key]  
        refcontent = sorted(refcontent, key=get_keyval, reverse=reverse) 
        info['content'] = refcontent


    def make_breadcrumbs(self):
        for info in self.fileinfo:
            breadcrumbs = []
            id = '' 
            comps = info['components'] 
            # discard index 
            if comps[-1] == 'index':
                comps = comps[:-1]
            for comp in comps: 
                id = id + '/' + comp
                breadcrumbs.append(self.site['reflinks'][id])
            info['breadcrumbs'] = breadcrumbs

    def make_pager(self):
        for info in self.navinfo:
            content = info['content']
            if not content:
                return
            content[0]['prev'] = None
            for i in range(1, len(content)):
                content[i-1]['next'] = content[i]
                content[i]['prev'] = content[i-1]
            content[-1]['next'] = None    

    def make_site(self):
        """Make the site."""
        # Keep sitedir alive if it exists, for the server
        if not os.path.exists(sitedir):
            os.mkdir(sitedir)
        make_clean(sitedir)
        ignore_patterns =  ('.*', '_*', '*.md', 'Makefile')
        ignore = shutil.ignore_patterns(*ignore_patterns)
        for fn in os.listdir(workdir):
            if any(fnmatch.fnmatch(fn, ip) for ip in ignore_patterns):
                continue 
            wp = os.path.join(workdir, fn) 
            sp = os.path.join(sitedir, fn)
            if os.path.isdir(wp):
                shutil.copytree(wp, sp, ignore=ignore)
            elif os.path.isfile(wp):
                shutil.copyfile(wp, sp)            
        self.process_content()

    def process_content(self):
        """Process the content files."""
        p = processors.ContentProcessor(sitedir, project=self)
        p.process()

# import pprint 

def build():
    proj = Project()
    proj.get_config()
    proj.get_siteinfo()
    proj.get_pythonhooks()
    proj.get_contentinfo()
    proj.resolve_reflinks()
    # pprint.pprint(proj.site['reflinks'])
    proj.make_breadcrumbs()
    proj.make_pager()
    proj.make_site()
