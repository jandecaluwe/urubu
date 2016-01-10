---
title: Markdown extensions
layout: page 
pager: true
author: Jan Decaluwe
---

Introduction
============

Urubu implements a number of Markdown extensions. These extensions do not
change or extend the Markdown syntax. Rather, they add interesting features by
processing and rendering the Markdown source in more sophisticated ways. 

The extensions are described in more detail below.

Project-wide reference ids
==========================

Urubu implements a Markdown extension to resolve project-wide reference ids.
This means that all pages in the project are automatically available as
reference ids, and can be referred to using Markdown's syntax for reference
links.

This feature is described in more detail in the sections
[/manual/structure#Project-wide reference ids] and [/manual/authoring#Reference
links]. It is Urubu's most important extension and a fundamental feature of the
tool.

Bootstrap-specific extensions
=============================

Urubu is designed to play well with [bootstrap].  To use certain Bootstrap
features, it has extensions that add Bootstrap classes to certain tags.
More specifically, the following classes are added:

table
:   Added to the `<table>` tag. This defines basic styling for tables.

dl-horizontal
:   Added to the `<dl>` tag that defines definition lists. This creates 
a horizontal layout for definition lists in wide viewports.

Support for the `<mark>` tag
============================

The html5 specification added _a new tag to highlight text_: the `<mark>`
tag. For a good explanation of its purpose and the differences with the
`<strong>` and `<em>` tags, see [this answer on Stack Overflow][mark]. 

[mark]: http://stackoverflow.com/a/14741437

Urubu supports lightweight markup for this tag by taking advantage of a
redundancy in Markdown. In standard Markdown, you can either use asterisks
(`*`) or underscores (`_`) to indicate emphasis. With the Urubu extension, the
underscore (`_`) version is rendered using `<mark>` instead.

This is an experimental feature that may be taken out if there are
serious objections, although at this point there do not seem to be
disadvantages. To disable the feature, the `mark_tag_support` variable
can be set to `false` in the `_site.yml` file. 

