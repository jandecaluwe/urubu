---
title: Project structure
layout: page
pager: true
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

* a `Makefile` is ignored and not copied to the build.

* files and directories starting with a dot `.` or
underscore `_` are ignored and not copied to the build.

* Markdown files with extension `.md` are converted to a
html file that is put into the build in the same relative location.

* all other files and directories are copied unmodified to the build in the
same relative location.

As a result of the project organization and the build process, the structure of
the build matches the structure of the project directory.  The relative
location of all files is thus preserved.

Special files and directories
=============================

`_site.yml`
-----------

This file contains site configuration info in YAML format.
Currently, these are the predefined attributes:

Attribute           | Description
--------------------|-------------
`reflinks`          | Holds a mapping from reference ids to link objects.
`baseurl`           | Prefix for generated local URLs
`file_ext`          | Change default file extension (`'.html'`) for processed `.md` files
`link_ext`          | Change default file extension (`'.html'`) for links to site's pages
`ignore_patterns`   | List of additional file names or globs to be ignored during processing
`keep_files`        | List of explicit file names be kept, overriding any ignores
`strict_undefined`  | Set the default behavior regarding undefined template variables


Link objects, for the `reflinks` attribute, are a mapping with an `url` key that maps
to the link URL and a `title` key that maps to the link title.

The `baseurl` option mirrors the same feature in [Jekyll][jekyll-options].  It
allows you to specify a prefix for all local URLs generated within your site.
This is necessary when your site will be served from a URL that has more than
just the hostname. For example, on GitHub Pages sites are served from
http://username.github.io/project_name/, so Urubu needs to include that
`/project_name/` in generated URLs pointing to local content.

`baseurl` should be specified with no beginning or trailing slashes, e.g.:

```yaml
baseurl: prefix
```
[jekyll-options]: http://jekyllrb.com/docs/configuration/#serve-command-options

The file extension attributes, `file_ext` and `link_ext`, are both usually set to the
same value (i.e. `'.php'`), unless the target site has .htaccess rewrite rules that
affect the file extensions.

Examples of this are sites that internally redirect pages like `www.test.com/account`
to `www.test.com/account.htm`. For this case, one would need to set `file_ext` to
`'.htm'`, so Urubu generated files have the `.htm` extension, whereas `link_ext` would
be set to `''`, so that the `a href` links are directed to the files without extension.

Otherwise, `file_ext` and `link_ext` should be set to the same extension, specially
during testing, so that the simple web server invoked by `urubu serve` works fine,
as well as any web server that does not rewrite the file extensions of the requests.

The `ignore_patterns` attribute specifies glob-style patterns to be ignored
during processing, in addition to the default ones according to the
[#Processing Rules].

In some cases you may explicitly want to keep certain files that would normally
be ignored. For example, you may have hidden files like `.nojekyll` to prevent
Jekyll processing, or `.htaccess` and `.htpasswd` for access control.  You can
keep such files in the build using the `keep_files` attribute.

The `strict_undefined` attribute controls whether the build should
silently ignore undefined template variables or raise an error when they are
encountered. If `false` or undefined, undefined template variables are treated
as empty strings (`''`). If `true`, the build will stop and raise an error.

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

file_ext: '.htm'  # Change default file extension ('.html')
link_ext: '.htm'  # Change default link extension ('.html')
```

`_layouts`
----------

This directory contains the available layouts.
They are used by the Jinja2 template engine to render html pages.
The layout files should have the `.html` extension.

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
`layout`   | Specifies the layout, without the `.html` extension, or `null`. Mandatory.
`date`     | Specifies the date in YYYY-MM-DD format. Optional.
`tags`     | A tag or list of tags for the content.
`saveas`   | Allows overriding of the output filename.

The `layout` attribute is mandatory, but can be given a `null` value.
This is useful when the page content is used by other pages, but
no html output is required for the page itself.

In addition, you can add arbitrary user-defined attributes. All attributes
are made available as page object attributes to the template engine.

Markdown in attributes
======================

Optionally, you can use markdown format in front matter attributes.  Markdown
processing is enabled by adding a `.md` suffix to the attribute. The resulting
html code will be stored in a synthesized attribute without the `.md` suffix.

For example:

```
---
title:
layout: page
summary.md: |
    A summary of the page items as a list:

    * item 1
    * item 2
    * item 3
---
```

After processing, the page object will have a `summary` attribute with the html
code.

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

A local link object is a mapping with either a `url` key to an url, or a `ref`
key to a reference id as mandatory items. In addtion, you can specify a title
with a `title` key.

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

Tag directory
=============

The optional top-level directory called `tag` has a predefined meaning.  Urubu
uses the corresponding folder in the build to hold the tag-related content view
that it generates automatically. You can use the index file to set attributes
such as the `layout`. However, the content will be generated by Urubu
automatically and needs not be set.


