---
title: Authoring
layout: manpage 
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
* [abbrev]
* [def_list]
* [fenced_code] 
* [code_hilite]
* [markdown_checklist]

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

Urubu extends this behavior by automatically resolving project-wide
reference links. (See the chapter about [structure]).

This feature is implemented as a Markdown extension. Note that it doesn't
require a syntax change. It enables page linking similar to what is commonly
found on wikis.

When you using reference links, Urubu will insert the title of the link in the
generated html (unless you specify an alternative text explicitly).  In this
way, the text that you click will match the title of the page where you land.
