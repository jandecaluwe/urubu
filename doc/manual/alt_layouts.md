---
title: Alt Layouts 
layout: page 
author: Jay Shafstall
---

# Alt Layouts

Alt Layouts are for when you want to create more than one physical .html file per .md file.  This is most useful when the additional .html files do not depend on the content of the original page, but on the front matter attributes.

## Usage

To enable alt layouts for a .md file, add an `alt_layouts` attribute to the front matter of a page.  This is a list of objects containing two attributes, `layout` and `location`.

The `layout` attribute gives the name of an alternate layout to use.  The `location` attribute gives the directory where the .html file should be put.  That directory must already exist in your directory structure.

Also add either `items_index` or `items_filter` to say where the list of it

## Example

The following is a sample of generating two additional .html files for a product page:

```
layout: product

alt_layouts:
    - layout: confirmation
      location: confirmations
    - layout: product_details
      location: details
```

If the original foo.md file was in the products directory, three .html files would be generated:

```
products/foo.html
confirmations/foo.html
details/foo.html
```
