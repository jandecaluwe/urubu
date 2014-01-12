---
title: Read me first
layout: article 
date: 2014-01-10
---

What is Urubu?
==============

Urubu is a tool to build static websites. The following sections will help you
to decide whether it is the right tool for you.

Static versus dynamic
=====================

A static website is the simple case. It consists of a set of fixed pages. The
only job of the web server is to serve the page that you request.

The opposite is a dynamic website. In this case, you interact with a program on
the web server. Depending on the request, the web server program generates a
response page on the fly.

Clearly, a dynamic website supports a much more interactive and sophisticated
web experience. If this is what you need, you should consider a full-fledged
CMS or CMS generator tool. There is a [wide choice][cms_list] of them in the Python
world. 

[cms_list]: https://wiki.python.org/moin/ContentManagementSystems

On the other hand, a static website is great for performance, security and
maintainability. If you don't need the overhead of a dynamic CMS, it is a
wise choice.

Why a tool?
===========

One option is to write a static website by hand by editing the html code for
each page. However, this quickly becomes an unpractical solution for two
reasons.

First, writing html is no fun. The markup overhead is error prone and makes it
difficult to read the actual content.  In Urubu, you use [markdown] for
authoring instead.  Markdown is an almost zero overhead input format and feels
like a natural way to write content in plain text. 

Secondly, html pages have a lot of non-content overhead that is equal or
similar across pages, such as navigation info. Duplicating and maintaining this
info manually is error prone and time consuming. In Urubu, you use templates
(also known as layouts) instead. They make it easy to define the common html
structure of a set of similar pages. 

Why Urubu?
==========

There is no shortage of static web site generators, including
a lot of [Python solutions][tool_list].   

[tool_list]: https://wiki.python.org/moin/PythonBlogSoftware#Static

However, these tools are typically blog oriented. If you think of your website
primarily as blog, with content in reverse chronological order and with good
support for tagging and archiving, there are probably better solutions than
Urubu.

On the other hand, if you think of your website as set of logically connected
content pages, Urubu may be a good choice. Urubu makes it it easy to define a good
navigation structure, so that a user is never "lost". This is especially
important for technical content.

Of course, it is possible to include a simple blog in an Urubu site.
Within a folder, you can specify how the content should be ordered using
an arbitrary key. For a blog, this would be reverse order by date.

Urubu's ideal use case
======================

If you would like to develop a website like a software project, you will feel
at home with Urubu. For example, you can maintain an Urubu site in a git or
mercurial repository and use the workflows that these systems enable.  For
example, you can collaborate on [github] or [bitbucket] through [pull
requests]. Also, deployment can be as straightforward as pushing to an upstream
repository. 

[pull requests]: https://help.github.com/articles/using-pull-requests
