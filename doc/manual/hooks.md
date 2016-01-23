---
title: Python hooks 
layout: page 
pager: true
author: Jan Decaluwe
---

Introduction
=============

Urubu supports Python hooks to make templating easier. Upon a build, it tries
to import a `_python` module or package, and looks for hook variables with
predefined names.  The following hooks are defined:

Variable              | Description
----------------------|-------------
`filters`             | A mapping from filter names to filter functions.
`process_info`        | A function to inspect and process content file info. 

You have to make sure that these names are exported correctly.  For example, if
you organize `_python` as a package, it could look as as follows:

```
_python/
    __init__.py
    filters.py
    hooks.py
```

If `filters` is defined in `filters.py`, and `process_info` in `hooks.py`, the
`__init__.py` file would contain:

```
from .filters import filters
from .hooks import process_info
```

The `filters` hook
==================

Filters functions should be defined as [custom filters in
Jinja2][jinja2_filters].

[jinja2_filters]: http://jinja.pocoo.org/docs/api/#custom-filters

As a typical example, consider a filter that converts a date value into a
desired format. The `filters.py` module would contain the following:

```
def dateformat(value, format="%d-%b-%Y"):
    return value.strftime(format)

filters = {}
filters['dateformat'] = dateformat
```

You can then use the `dateformat` filter in templates.

The `process_info` hook
=======================

The interface of the `process_info` function is as follows:

```
def process(info, site):
    ...
```

This function is called for every content file in the project.

The `site` variable provides access to the site variables defined in
`_site.yml`.

The `info` variable contains the file content info as it is being
constructed by Urubu. At the moment of the call, the following
inferred attributes are available:

Attribute      | Description 
---------------|---------------------------
`id`           | The unique id by which the object is known in the project. 
`url`          | The url of the object. 
`components`   | The components of the object's pathname, without file extension, as a list.
`fn`           | The pathname of the file or directory corresponding the object. 
`mdate`        | Modification date

In addition, all attributes specified in the YAML front matter of the
corresponding content file are available as attributes of the `info` object.

The `site` and `info` variables are Python dictionaries. This means that the
attributes are available via key access, not via Python attribute access.  This
is because the YAML reader constructs Python dictionaries from the front
matter.

The `process_info` function can can inspect the attributes, verify and modify
them, and add additional ones.

`process_info` examples
=======================

Defining a default `layout`
---------------------------

It can be handy to define a default `layout` for the case this mandatory
attribute is not specified in the content file.  Suppose we want a default
`index` layout for index files, and a `page` layout for other files:

```
def process_info(info, site):
    if 'layout' not in info:
        if info['components'][-1] == 'index':
            info['layout'] = 'index'
        else:
            info['layout'] = 'page'
```

Defining a specific layout 
--------------------------

Suppose we have a `blog` directory and we want to automatically define a
specific `post` layout for blog posts:

```
def process_info(info, site):
    components = info['components']
    if len(components) == 2:
        if components[0] == 'blog' and components[1] != 'index':
            process_post(info)

def process_post(info):
    if not 'layout' in info:
        info['layout'] = 'post'
```



 

