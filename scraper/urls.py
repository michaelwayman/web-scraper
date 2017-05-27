"""
Utilities to handle and deal with URLs.
"""

import re
from urllib.parse import urljoin, urlparse


class Url:
    """ Validation, normalization of a URL.

    Note on Url "uniqueness":
        >>> Url('http://google.com') == Url('https://google.com') == Url('https://google.com?q=shark+week')
        True
    """
    def __init__(self, url):
        self.url = url.lower()
        parsed = urlparse(self.url)
        if not parsed.netloc:
            raise ValueError(f'{self.url} is not a complete URL.')

    def normalized(self):
        parsed = urlparse(self.url)
        return f'http://{parsed.netloc}{parsed.path}'

    def __hash__(self):
        return hash(self.normalized())

    def __eq__(self, other):
        return self.normalized() == other.normalized()

    def __str__(self):
        return self.normalized()

    def __repr__(self):
        return self.normalized()


def url_filter(url):
    """ Filter to remove non HTML URLs """
    if url.endswith(('.json', '.css', '.png', '.jpg', '.svg', '.ico', '.js', '.gif', '.pdf', '.xml')):
        return False
    if url.startswith(('mailto',)):
        return False
    return True


def urls_from_html(html, html_url, Class_=Url):
    """ Parses HTML for URLs

    Args:
        html (str): HTML content
        html_url (str): URL of the HTML content. Required to create full URLs from relative paths.
        Class_ (class): The type of URL objects to return

    Returns:
        ([Class_]) list of Class_ instances.
    """

    urls = re.findall(r'href="(.*?)"', html)

    # build absolute URLs from relative paths
    for i, url in enumerate(urls):
        parsed = urlparse(url)
        if not parsed.netloc:
            urls[i] = urljoin(html_url, url)

    # Create `Class_` instances from URLs we found in the HTML
    unique = set()
    for u in urls:
        try:
            if url_filter(u):
                unique.add(Class_(u))
        except ValueError:
            pass

    return list(unique)
