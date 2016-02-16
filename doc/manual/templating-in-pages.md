---
title: Templating constructs in pages
layout: page 
pager: true
author: Jan Decaluwe
---

{% from 'util.html' import open, done, fa, figure %}

Overview
========

Writing in Markdown is great, but sometimes you run into limitations. For those
cases, Urubu supports a feature gratefully borrowed from [jekyll]: using
templating constructs in content pages.

Basically, all content pages are processed by the templating engine before
going to the Markdown processor. The full power of [jinja2] is thus available
in your content pages. 

The usage of templating constructs in content pages is best explained with
examples. Therefore, we will start with some examples, and review the concepts
afterwards.

Example usage
=============

Task list icons
---------------

Suppose you want to emulate [github] style task lists, as follows:

* {{ open }} Task 1
* {{ done }} Task 2
* {{ open }} Task 1

An icon is used to show whether a task is still open or not. 

We can support this by defining well-named reusable variables in a dedicated
template file, as follows:

```
{% raw %}
{% set open = '<i class="fa fa-square-o"></i>' %}
{% set done = '<i class="fa fa-check-square-o"></i>' %}
{% endraw %}
```

Variables `open` and `done` now hold HTML code that refers to icons. In these
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

Within the content page, we can use the variables as follows, to get the result
as above:

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
refer to any icon by name. This can be done with a Jinja2 macro. A macro is
like a function that can take parameters:

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
`<figcaption>` tag to add captions. We can support this with the following
macro:

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

This macro assumes that images will be placed in an `img/` directory. In
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

Templating concepts
===================

Template processing is done first
---------------------------------

The examples illustrate how you can use template variables and macros to
construct HTML code. However, it is important to understand that template
processing is done first, before Markdown processing (for good reasons).  Thus,
the HTML code from variables and macros first becomes part of Markdown source
code.  This works well because Markdown is designed to handle HTML
transparently.

Full template power available
-----------------------------

The examples demonstrate the use of variables, macros, and imports.  This is
merely the beginning: in fact, the full power of Jinja2 templates is available.
This is a vast subject. To learn what is possible, see the [Jinja2 Template
Designer Documentation][jinja2_templates].

Context variables
-----------------

When Urubu invokes template processing on a page, it automatically passes
certain context variables.  This works exactly like for regular templates, as
described in [/manual/templates#Context Variables]. Basically, variable `this`
provides access to the page attributes, and variable `site` provides access to
the global site attributes. 

Template delimiters
-------------------

Template support introduces new delimiters as follows:

{% raw -%}
* `{# ... #}` for comments not included in the output
* `{{ ... }}` for expressions, to print to the output
* `{% ... %}` for statements
{% endraw %}

These delimiters deserve some attention.

{# Now commenting about comments #} 

First, the comment delimiters are interesting because they add a functionality
that is not available in Markdown: comments that will not show up in the
output.

Secondly, as always with delimiters, there is the problem of how to escape them
if you want to use them literally in source code, without interpretation.

For an inline literal or snippet you can use literal expressions.  For example,
to get `{{ '{{' }}` you can write {% raw %} `{{ '{{' }}` {% endraw %}.   

For a larger section, you can mark a block *raw*. For example, to
get the list shown earlier in this section, you can write:

```
{{ '{% raw %}' }}
{% raw -%}
* `{# ... #}` for comments not included in the output
* `{{ ... }}` for expressions, to print to the output
* `{% ... %}` for statements
{% endraw %}
{{ '{% endraw %}' }}
```

[jinja2_templates]: http://jinja.pocoo.org/docs/dev/templates


