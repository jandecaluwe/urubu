---
title: How do I make a sitemap?
layout: page
date: 2016-07-04
---

To generate a sitemap you need to do the following:

* Create a markdown file called `sitemap.md` like this:
```
---
title: sitemap
layout: sitemap
changefreq: monthly
priority: 1.0
xmlns: http://www.google.com/schemas/sitemap/0.84
saveas: sitemap.xml
---

```

* Provide a `sitemap.html` in the `_layouts` directory, with looking something like the following:
```
{% raw %}
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="{{ this.xmlns }}">
{% for t in site.reflinks %}
    {% if site.reflinks[t].fn and not site.reflinks[t].hidden %}
    <url>
        <loc>{{ site.hostname }}{{ site.reflinks[t].url }}</loc>
        <changefreq>{{ this.changefreq }}</changefreq>
        <priority>{{ this.priority }}</priority>
    </url>
    {% endif %}
{% endfor %}
</urlset>
{% endraw %}
```

What makes this work is for the main part the `saveas` parameter in the `sitemap.md` file, which overrides the default output filename with `sitemap.xml` instead of `sitemap.html`

