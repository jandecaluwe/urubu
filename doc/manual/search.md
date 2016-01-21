---
title: Adding Search 
layout: page 
pager: true
author: Jan Decaluwe
---

Introduction
============

A static site cannot natively support dynamic services. Fortunately, it is
often an elegant solution to integrate third party solutions within a
static site.

One of the most prominent examples is Search. One possibility is integrating an
external service such as Google Custom Search. The disadvantage is that one has
either to pay for it or accept the branding.  

As an alternative, Urubu supports Tipue Search, an open source solution based
on javascript executed in the browser. As part of the site building, Urubu
generates a view on the searchable content.  In this chapter, we describe how
the integration is accomplished.  

Installing Tipue Search
=======================

The first step is to [download][1] the Tipue Search distribution It contains a
`tipuesearch` directory. Copy that directory to the top level of your project.
As usual, Urubu copies it to the built website, so that the required
stylesheets and javascript files are available in the expected location.

Do not rename the `tipuesearch` directory. The existence of that
directory triggers Urubu's support. 

Tipue Search has good [documentation][2] that you may want to review.  This
chapter uses a slightly modified approach to achieve a good integration in a
typical Urubu project. 

The search box
==============

The next step is to create a search box. Suppose you want to make it part of
the navbar, as in the present site. This is achieved with the following html
code: 

```
<form class="navbar-form navbar-left" action="/search.html" role="search">
  <div class="form-group">
    <input type="text" required name="q" id="tipue_search_input" class="form-control" placeholder="Search"> 
   </div>
</form>
```

The `name` and the `id` values in the `<input>` tag of the search box are
mandatory for Tipue Search. The typical place for this code would be in the
navbar code in a basic layout for the site.

The search results page
=======================

The next step is to create a search result page. To integrate it we first
create a dedicated layout using template inheritance.  Let us assume that is
there is  a `head_addon` and a `body_addon` block to add links and scripts to
the `<head` and the `<body>` section respectively. The `search.html` layout is
then as follows:  

```
{% raw %}
{% extends "page.html" %}

{% block head_addon %}
<link href="tipuesearch/tipuesearch.css" rel="stylesheet">
{% endblock %}

{% block body_addon %}
<script src="tipuesearch/tipuesearch_content.js"></script>
<script src="tipuesearch/tipuesearch_set.js"></script>
<script src="tipuesearch/tipuesearch.min.js"></script>
<script>
$(document).ready(function() {
     $('#tipue_search_input').tipuesearch({
          'mode': 'json',
          'contentLocation': 'tipuesearch/tipuesearch_content.json' 
     });
});
</script>
{% endblock %}
{% endraw %}
```

We inherit from a `page.html` layout. In the `head_addon` block, we add
the Tipue Search style sheet for the result page. In the `body_addon` page we
add the Tipue Search java script modules, and the inline script that generates
the results. 

This setup assumes that the jQuery javascript library itself is already loaded
in the body of the parent layout, with a line like the following: 

```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
```

If you use the Bootstrap javascript modules, that will be the case.

In the top level project directory, we can then create a `search.md` files that
uses the `search.html` layout and has the generated search results as its
content:

```
---
title: Search results
layout: search
---

<div id="tipue_search_content"></div>

```

After building the site, there will be a functional `search.html` file in the
top-level directory.

**Note** The `tipuesearch.css` stylesheet also contains styling for the search
box. The result may be undesirable if you use your own styling, like in the
present website. The workaround is to comment the search box styling out. 
{.text-info}

The search content
==================

The searchable content itself is a JSON object defined in the file
`tipuesearch/tipuesearch_content.json`.  This is where Urubu kicks in: this
file is generated automatically. 

Extracting meaningful searchable content from a web site is not trivial. A
design decision for Urubu was to use modern techniques to help with this. In
particular, Urubu will only consider content that is wrapped with the `<main>`
tag. This is a relatively new html5 tag with exactly the purpose to indicate
the page content explicitly.

The site designer should therefore review the site layouts and wrap all
searchable content with the `<main>` tag. Typically, this is the region were
the `this.body` variable is called in a template.

**Note** The `<main>` tag is not supported in IE11. A popular workaround is to
use the `html5shiv.js` Javascript module. Layouts based on Bootstrap do
this already.
{.text-info}

[1]: http://www.tipue.com/search/
[2]: http://www.tipue.com/search/docs/
