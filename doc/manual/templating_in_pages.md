---
title: Templating in pages
layout: page 
pager: true
author: Jan Decaluwe
---

{% from 'util.html' import open, done, fa, figure %}

Overview
========

Writing in Markdown is great, but sometimes you will run into limitations. For
those cases, Urubu supports a feature gratefully borrowed from [jekyll]: using
templating constructs in content pages.

Basically, all content pages are processed by the templating engine before
going to the Markdown processor. The full power of [jinja2] is thus available
in your content pages. 

Usage
=====

The usage of templating constructs in content pages is best described with a
number of examples.

Task list icons
---------------

Suppose you want to emulate [github] style task lists, as follows:

* {{ open }} Task 1
* {{ done }} Task 2
* {{ open }} Task 1

An icon is used to show whether a task is still open or not. 

We can support this by defining well-named reusable variables in a dedicated
layout file, as follows:

```
{% raw %}
{% set open = '<i class="fa fa-square-o"> </i>' %}
{% set done = '<i class="fa fa-check-square-o"></i>' %}
{% endraw %}
```

Variables `open` and `done` now hold HTML that refer to icons. In these
examples, I use the [font-awesome] icon  library. You will need to add the
appropriate reference to the icon stylesheet in your base template. 

Suppose these variables are defined in the file `_layouts/util.html`. We can
import them in any content page as follows:

```
{% raw %}
{% from 'util.html' import open, done %}
{% endraw %}
```

Note that Urubu knows to look up `util.html` in the `_layouts/` directory,
because that is where templates should be located. 

Within the content page, we can use the variables as follows, to give the
results as above:

```
{% raw %}
* {{ open }} Task 1
* {{ done }} Task 2
* {{ open }} Task 1
{% endraw %}
```

General icon interface
----------------------

Suppose you want a more general interface to icons, so that you can easily
refer to any icon by name. This can be done by using a Jinja2 macro. A macro
is like a function that can take parameters:

```
{% raw %}
{% macro fa(name, class='') %}
<i class="fa fa-{{name}} {{class}}"></i>
{% endmacro %}
{% endraw %}
```

Again, we can import the macro `fa` in content pages:

```
{% raw %}
{% from 'util.html' import fa %}
{% endraw %}
```

Then we can use it as follows, for example to refer to the Github icon:

```
{% raw %}
{{ fa('github') }}
{% endraw %}
```

This gives the following result:

{{ fa('github') }}

We can pass additional CSS classes via the optional `class` parameter. The
following example gets the alternative Github icon in twice the basic size:

```
{% raw %}
{{ fa('github-alt', 'fa-2x') }}
{% endraw %}
```

This gives the following result:

{{ fa('github-alt', 'fa-2x') }}

Figure
------

Standard Markdown does not support the HTML5 `<figure>` tag, and the related
`<figcaption>` tag to add captions. We can support this with the
following macro:

```
{% raw %}
{% macro figure(fn, caption='') %}
<figure>
  <img src="/img/{{fn}}" class="img-responsive" alt="{{caption}}">
  {% if caption %}
  <figcaption class="text-center">{{caption}}</figcaption>
  {% endif %}
</figure>
{% endmacro %}
{% endraw %}
```

This macro assumes that images will be places in an 'img/' directory. In
addition, it makes the image responsive using a Bootstrap class, and centers
the optional caption.  Again, we can use the macro by importing:

```
{% raw %}
{% from 'util.html' import figure %}
{% endraw %}
```

This is an example usage:

```
{% raw %}
{{ figure('urubu.jpg', "An Urubu - a brazilian vulture") }}
{% endraw %}
```

This gives the following result:

{{ figure('urubu.jpg', "An Urubu - a brazilian vulture") }}

