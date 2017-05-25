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
