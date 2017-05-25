import os
import unittest

from schireson.urls import urls_from_html, Url


class TestUrlsFromHtml(unittest.TestCase):
    """
    Tests `urls_from_html` function
    """

    def _html(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        test_file_path = os.path.join(base_path, 'test_data', 'test.html')
        with open(test_file_path, 'r') as f:
            return f.read()

    def setUp(self):
        self.test_html = self._html()

    def test_urls(self):
        urls = urls_from_html(self.test_html, 'http://foobar.com/')
        urls = {x.url for x in urls}
        self.assertSetEqual(
            urls,
            {'https://my.3rdpartyblog.com', 'http://foobar.com/index.html',
             'http://foobar.com/?q=local_query', 'http://foobar.com/about'}
        )


class TestUrl(unittest.TestCase):
    """
    Tests `Url` class
    """

    def test_normalized(self):
        url = Url('https://m.facebook.com/mike.test?q=hello&foo=bar')
        self.assertEquals(url.normalized(), 'http://m.facebook.com/mike.test')

        url = Url('https://www.facebook.com/mike.test/wow/')
        self.assertEquals(url.normalized(), 'http://www.facebook.com/mike.test/wow')

    def test_complete_url_assertion(self):
        with self.assertRaises(ValueError):
            Url('fb.com/mike.test')

    def test_hash(self):
        url1 = Url('https://m.facebook.com/mike.test')
        url2 = Url('https://m.facebook.com/mike.test?q=q1')
        url3 = Url('https://m.facebook.com/mike.test?q=q2')

        s = {url1, url2, url3}
        self.assertEquals(len(s), 1)

    def test___eq__(self):
        url1 = Url('https://m.facebook.com/mike.test')
        url2 = Url('https://m.facebook.com/mike.test?q=q1')
        url3 = Url('https://m.facebook.com/mike.test?q=q2')

        self.assertTrue(url1 == url2 == url3)
