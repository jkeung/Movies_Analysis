# Movies Analysis
Analysis of movies using data webscraped from boxofficemojo.com. Parallelize scraping using Luigi!

# Clone the repository

```$ git clone https://github.com/jkeung/Movies_Analysis.git```

## Setup

This code is portable across the following OS's: Linux distributions, Mac and Windows OS's. Scripts were written using Python 2.7 and have not been tested for portability to Python 3.X.

You are encouraged to use a python virtual environment using virtualenv and pip. 

```$ virtualenv movies_analysis```

### Install requirements:

```$ pip install -r requirements.txt```

#### Description of modules imported and application

* backports-abc - A backport of recent additions to the 'collections.abc' module
* backports.ssl-match-hostname - The ssl.match_hostname() function from Python 3.5
* beautifulsoup4 - Beautiful Soup sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree
* certifi - Python package for providing Mozilla's CA Bundle
* docutils - Docutils is a modular system for processing documentation into useful formats, such as HTML, XML, and LaTeX
* lockfile - Platform-independent file locking module
* luigi - Luigi is a Python (2.7, 3.3, 3.4) package that helps you build complex pipelines of batch jobs. It handles dependency resolution, workflow management, visualization, handling failures, command line integration, and much more
* python-daemon - Library to implement a well-behaved Unix daemon process.
* python-dateutil - Extensions to the standard Python datetime module
* requests - Requests is an Apache2 Licensed HTTP library, written in Python, for human beings
* singledispatch - This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3
* six - Python 2 and 3 compatibility utilities
* tornado - Tornado is a Python web framework and asynchronous networking library, originally developed at FriendFeed
* wheel - A built-package format for Python

## Run Parallelized Scraping Script via Spotify's Luigi Package

#### First, launch Luigi Daemon

``` $ luigid ```

#### Next, run scraping script locally with 4 workers

```
$ python scrape_movie.py --workers=4 --local-scheduler

```

View dependency tree and status of job at http://127.0.0.1:8082/
