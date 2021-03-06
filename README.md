# Radiopadre: Python Astronomy Data & Results Examiner

Astronomy visualization framework for ipython notebooks.

[![Build Status](https://travis-ci.org/radio-astro/radiopadre.svg?branch=master](https://travis-ci.org/radio-astro/radiopadre)

[radiopadre on pypi](https://pypi.python.org/pypi/radiopadre)

Radiopadre is a framework, built on the Jupyter notebook, for browsing and visualizing data reduction products. It is particularly useful for visualizing data products on remote servers, where connection latencies and/or lack of software etc. limits the usual visualization options. It includes integration with the JS9 browser-based FITS viewer (with CARTA integration coming soon).

The general use case for Radiopadre is "here I am sitting with a slow ssh connection into a remote cluster node, my pipeline has produced 500 plots/logs/FITS images, how do I make sense of this mess?" More specifically, there are three (somewhat overlapping) scenarios that Radiopadre is designed for:

* Just browsing: interactively exploring the aforementioned 500 files using a notebook.

* Automated reporting: customized Radiopadre notebooks that automatically generate a report composed of a pipeline's outputs and intermediate products. Since your pipeline's output is (hopefully!) structured, i.e. in terms of filename conventions etc., you can write a notebook to exploit that structure and make a corresponding report automatically.

* Sharing notebooks: fiddle with a notebook until everything is visualized just right, insert explanatory text in mardkdown cells in between, voila, you have an instant report you can share with colleagues.

## Usage, in a nutshell

Assuming everything is installed (see below), then to view data on your local machine:

```
$ run-radiopadre <directory>[/<notebook>.ipynb]
```

To view data on a remote machine (to which you have ssh access):

```
$ run-remote-padre <hostname>:[<directory>[/<notebook>.ipynb]]
```

This should open up a Jupyter tab in your local browser.

## Installation

The easiest way to start is to use the Docker images, see below.

On your local machine, install radiopadre with pip or from source (see below).

On the remote machine, either use the Docker images, or install radiopadre with pip 
or from source (see below). The latter can be useful if you want to e.g. 
track a development branch etc.

### Installing from pip

```
$ pip install radiopadre
```

### Installing from source

Use this if you want to track the git repository (i.e. latest and greatest version, or perhaps a development branch).

* prerequisites: ``git``, ``pip``, ``virtualenv``. For JS9 support, 
also ``libcfitsio-dev`` and ``nodejs``, unless you use docker. 

* ``git clone https://github.com/ratt-ru/radiopadre-devel radiopadre`` or ``git clone https://github.com/ratt-ru/radiopadre`` (depending on which repo you track)

* put the resulting ``radiopadre/bin`` directory into your path

* run ``install-radiopadre``

This should create a radiopadre virtual environment (under ``~/.radiopadre/venv``) and prepare it for running radiopadre.

**Tracking updates:** If you use ``git pull`` to pull in changes, you may sometimes need to run ``install-radiopadre reinstall`` to reinitialize the virtual environment. For minor updates this is not usually needed, so you can skip it if you're feeling lazy (since the process takes a few minutes). When in doubt, reinstall. When unexpected errors arise, reinstall.


### Installing and using Docker images

This is probably the easiest way to run radiopadre. You don't even need a remote installation,
docker will take care of that for you. On your local client, all you need is to 
``pip install`` or ``git clone`` the source, and you don't even need to set up the virtual 
environment -- all you need, actually, are are the two run scripts. Then use the ``-d`` flag:

```
$ run-radiopadre -d <directory>[/<notebook>.ipynb]
```

To view data on a remote machine (to which you have ssh access):

```
$ run-remote-padre -d <hostname>:[<directory>[/<notebook>.ipynb]]
```

In both cases a Docker image will be downloaded (locally or remotely) as needed.

## Tutorial

For a quick tutorial on radiopadre, download one of the 
[tutorial packages](https://www.dropbox.com/sh/be4pc23rsavj67s/AAB2Ejv8cLsVT8wj60DiqS8Ya?dl=0), 
untar, and run radiopadre inside the resulting directory, locally or remotely (you can also refer to the PDF 
enclosed in the tarball for a poor man's rendering of the notebook).
