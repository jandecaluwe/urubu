---
title: How to preview sites that use the baseurl option?
layout: page
date: 2015-04-30
---

Urubu version 0.8 and higher
----------------------------

The `urubu serve` command  takes the `baseurl` setting automatically into
account. 

Urubu version 0.7
------------------

The `urubu serve` server does not include the `baseurl` prefix when serving
pages so sites that use `baseurl` can't be previewed locally using `urubu
serve`.  An alternative option is to use
[tservice](https://github.com/jiffyclub/tservice), which includes an option to
serve a local static site with a URL prefix.  To use tservice with an Urubu
site instead of using `urubu serve` call `tserve` with the prefix option, e.g.

```
tserve --prefix <baseurl> _build
```

Where `<baseurl>` is your site's particular prefix.
