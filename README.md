# Scraper

This is some python code that is capable of crawling and scraping dynamic Web sites.

**Dynamic Web sites** are sites that:
 - dynamically load content (e.g. gets search results from an AJAX call)
 - render their HTML using javascript (e.g. any reactjs Web site)

Scraper is able to scrape dynamic Web sites by loading the page in a virtual Webkit browser, allowing the JavaScript to run, before parsing the HTML.

**Crawling** - each URL that is found on a Web page is added to a queue to be rendered.

# Usage

You can use this code in one of two ways:
 1. Use scraper as a "program" and follow the command pattern provided.
 2. Import "scraper" yourself and use it as a library.

___

### As a program
```shell
python3 ./scraper -h
usage: scraper [-h] {}

Crawl and scrape dynamic Web sites. Scrape Web sites that dynamically load
content or sites that render their HTML using javascript. Either use the
command pattern provided or import "scraper" to use as a library.

positional arguments:
  {}  The command to run.

optional arguments:
  -h, --help  show this help message and exit
```

#### Commands

 - `TODO`

___

### As a library
example.py
```python

def callback(self, url, html):
    # url is the URL of the page that just finished rendering
    # html is the rendered HTML of the page, (at this point the page's dynamic content has already loaded into the HTML)
    do stuff...

scraper = DownloadScheduler(
    callback,
    initial=[Url('https://www.google.com/search?q=shark+week')],
    processes=4
)
scraper.schedule()
```

the `DownloadScheduler` parameters:
 - `callback` is called every time a page is rendered in our webkit engine.
 - `initial` is a list of `Url`s that we are going to start scraping/crawling at.
 - `processes` is the number of parallel processes we want to crawl/render with.

# Requirements

 - python 3.6+
 - pip dependencies
    - PyQt5==5.8.2
    - pyobjc==3.2.1 (mac only)
