---
title: Project building 
layout: page 
pager: true
author: Jan Decaluwe
---

The `urubu` command
===================

After installation, an `urubu` command will be available.

If you prefer, you can call the installed package as a script using `python -m
urubu`, with the same effect.

Subcommands
===========

The `urubu` command supports two subcommands. Run these commands from the top
level project directory.

`urubu build`
: Build the website.  The website will be in the `_build` subdirectory.

`urubu serve` 
: Start a local webserver to serve the website as you develop it.  The website
will be available at `localhost:8000`. Run this command in a separate terminal
window, and kill the server when you are done.

Development flow
================

I prefer to put the  commands in a Makefile, so that I can
run `make` to build and `make serve` to start a server.

Currently, you have to build the site explicitly to see
the development changes in the browser.

