---
title: Authoring
layout: page 
pager: true
author: Jan Decaluwe
---

Content 
=======

In Urubu, content is entered in [markdown] format. This is a lightweight format
that feels like a natural way to write content in plain text.

Stock markdown has a small feature set. For example, it does not even
support tables. For this reason, Urubu supports some extensions. In particular,
it supports the [markdown_extra] extensions that have become an industry
standard, as well as a few others.

The most notable supported extensions are:

* [tables]
* [attr_list]
* [abbrev]
* [def_list]
* [fenced_code] 
* [code_hilite]

Code
====

Urubu intents to offer good support for software projects. Therefore, it
supports nicely rendered code blocks. 

One part of the solution is [fenced_code], provided by the Markdown Extra
extensions.  This lets you enter language-specific code blocks without the need
for indentation.

The second part is the [code_hilite] extension of Python-Markdown.  This
extension enables language-specific syntax highlighting through the [pygments]
library.

To properly render the highlighted code, you will need to add a `syntax.css`
stylesheet. A good solution is to use the [syntax stylesheet from
GitHub][syntax_github].

[syntax_github]: https://github.com/mojombo/tpw/blob/master/css/syntax.css

Reference links
===============

Stock Markdown supports "reference links" that are resolved by defining them
later in the file. For example, you can use `[urubu]` in your content and
further on define it as follows:

```
[urubu]: http://urubu.jandecaluwe.com
```

This is nice for readability, but it all remains file based.

Urubu extends this behavior by automatically resolving [structure#Project-wide
reference ids].  This feature is implemented as a Markdown extension. Note that
it doesn't require a syntax change. It enables page linking like in wikis.

In addition, you can add a fragment, like `#some-anchor`, to the reference id.
This represents a link to an anchor within a page.  Since Urubu automatically
adds slugified anchors to markdown headers, you can use those as targets.  For
instance, `[authoring#reference-links]` is a link to the current
[authoring#Reference links] section.  You can also define your own anchors
using [attr_list]. 

Markdown supports reference links without a text.  In that case, Urubu inserts
an appropriate text in the html.  For a reference link with no fragment, the
title of the page is inserted.  For a reference link with a fragment, the
fragment text is inserted. To make the result more readable, you can use
non-slugified fragment text.  For example, `[authoring#Reference links]` also
links to the present section, and is rendered as [authoring#Reference links]. 
