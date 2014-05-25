---
title: Installation
layout: simple_page 
date: 2014-01-10
---

Urubu requires Python 2.7. It is developed with Python 3 in mind, but only
tested with Python 2.7.

You can install Urubu using pip: 

```
pip install urubu
```

To upgrade an existing installation to the
latest version, use:

```
pip install --upgrade urubu
```

If pip is not yet available on your system, follow the [pip installation
instructions][pip_install].

[pip_install]: http://www.pip-installer.org/en/latest/installing.html

You may want to install Urubu in an isolated environment using [virtualenv].

Urubu depends on a number of libraries that will automatically be installed if
not yet available: [python_markdown], [pyyaml], [pygments] and [jinja2].

For a quick way to set up a new Urubu project, visit [urubu-quickstart].
