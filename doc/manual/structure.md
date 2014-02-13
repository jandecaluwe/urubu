---
title: Project structure 
layout: manpage 
author: Jan Decaluwe
---

The project directory
=====================

A typical Urubu project directory looks as follows:

```
Makefile
_site.yml
_layouts/_base.html
         page.html
         ...
_python/__init__.py
        validators.py
        filters.py
css/...
js/...
index.md
folder1/index.md
        file1.md
        pic1.png
        ...
folder2/index.md
        file2.md
        file3.md
        ...
```

Files and directories with pathnames starting with an underscore `_` are
special. They are used during processing, but excluded from the built website.
Their function will be discussed below.  

The `css` and `js` directories are just an example of how CSS style sheets and
javascript files could be organized. You can use any organization that you
prefer.

Content files are in Markdown format and should have the `.md` extension. You
have complete freedom in organizing them in directories. However, every
directory should have an `index.md` file, including the top-level directory.

Processing rules
================

Urubu generates a website by processing the files and directory in the project
directory, and putting the result in a `_build` subdirectory. The processing
depends on the pathname as follows:

* a `Makefile` is not copied to the build. 
* files and directories starting with a
dot `.` or underscore `_` are not copied to the build.
* Markdown files with extension `.md` are converted to a
html file that is put into the build in the same relative location.
* all other files and directories are copied unmodified to the build in the
same relative location.

As a result of the project organization and the build process, the
structure of the build matches the structure of the project directory.
The relative location of all files is thus preserved.

Special files
=============

`_site.yml`
-----------

This file contains site configuration info in YAML format.
Currently, a single attribute is predefined: 

Attribute      | Description
---------------|-------------
`reflinks`     | Holds a mapping from reference ids to link objects.

Link objects are a mapping with an `url` key that maps to the link url and
a `title` key that maps to the link title. 

You can define additional attributes that will be made available as
site variables to the template engine. The following is an example of a
`_site.yml` file:

```
brand: Urubu 

reflinks:
    content_license:
        url: http://creativecommons.org/licenses/by-sa/3.0/
        title: CC-BY-SA License
    software_license:
        url: http://www.gnu.org/licenses/agpl-3.0.txt
        title: GNU Affero General Public License
    markdown:
        url: http://daringfireball.net/projects/markdown/  
        title: Markdown
```

`_layouts`
----------

This directory contains the templates that define the available layouts.
They are used by the Jinja2 template engine to render html pages.
The templates files should have the `.html` extension.

`_python`
---------
This directory contains Python hooks for the template engine. 

Project-wide reference ids 
==========================

Urubu has the concept of project-wide reference ids.  You can use them to refer
to link objects in your content and configuration.  Their definition comes
from two sources:

* global reference ids are mapped to link objects in the `_site.yml`
configuration file, as discussed earlier.
* all content pages and folders objects have reference ids.

Project-wide references ids live in a single namespace. For pages and folders,
the id is a root-relative pathname starting with a slash `/` and without file
extension. By convention, global reference ids should not start with a `/`.   

In your content and configuration info, you can also use relative reference
ids. Urubu will resolve them depending on the file location in the project. In
case of a name clash with a global reference id, you will have to disambiguate
by adding pathname components. 

In accordance with Markdown conventions, reference ids are case-insensitive.

Content files
=============

Content files are Markdown files with extension `.md`. They should start with
YAML front matter that defines a number of attributes, as in the following example:

```
---
title: Read me first
layout: page
date: 2014-01-15
---
<Markdown content>
```

The following attributes are predefined:

Attribute | Description
-----------|------------
`title`    | Specifies the page title. Mandatory.
`layout`   | Specifies the desired layout, without the `.html` extension. Mandatory.
`date`     | Specifies the date in YYYY-MM-DD format. Optional.
`tags`     | Reserved for future use.

In addition, you can add arbitrary user-defined attributes. All attributes 
are made available as page object attributes to the template engine.

Index files
===========

Index files with basename `index.md` are a special kind of content files.  They
are used to specify the attributes and the content of a directory. There are
two options to specify the content, explicitly with the `content` attribute or
implicitly using the `order` attribute.  

Attribute | Description
-----------|------------
`content`  | Defines the content explicitly as a list of reference ids or local link objects.
`order`    | Defines the attribute by which the content in the directory should be ordered.
`reverse`  | Optional boolean attribute defines reverse order or not. Default is `false`.

`content` and `order` are mutually exclusive; you should use one of the two options.

A local link object is a mapping with a `url` key to an url, and a `title` key
to a title.  Alternatively, you can start from an existing reference id
using a `ref` key, and overwrite its title.  

The ordering attribute can be predefined or user-defined, but it should be
specified in each content file in the directory.  As an example, you can
specify that the content of a directory should be ordered as blog by the
following front matter in the index file: 

```
---
title: Blog
layout: blog_index
order: date
reverse: true
---
```


