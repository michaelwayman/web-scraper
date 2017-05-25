"""
Module schedules Web page downloads.
it "crawls" new links it discovers.
And routes downloaded Web pages to appropriate callbacks.

# Example Usage
```
def callback(url, success, html):
    print(html)

s = DownloadScheduler(callback, initial=['https://www.google.com/search?q=shark+week'])
s.schedule()
```
"""
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import subprocess

from urls import urls_from_html


class DownloadScheduler:

    def __init__(self, callback, initial=None, processes=5):
        """ DownloadScheduler downloads Web pages at certain URLs
        Schedules newly discovered links, adding them to a queue, in a "crawling" fashion
        Args:
            callback (func): Callback function whenever a Web page downloads
            initial ([Url]): List of `Url`s to start the "crawling"
            processes (int): The maximum number of download processes to parallelize
        """
        self.callback = callback
        self.queue = deque(initial or [])
        self.visited = set()
        self.processes = processes

    def download_complete(self, future, url):
        """ Callback when a download completes
        Args:
            future (Future): the (completed) future containing a Web site's HTML content.
            url (Url): the URL of downloaded Web page.
        """
        try:
            html = future.result()
        except Exception as e:
            print(f'Exception {e}')
        else:
            urls = urls_from_html(html, url.url)
            self.queue.extendleft(urls)
            self.callback(url.url, html)

    def schedule(self):
        """ Begins downloading the Web pages in the queue.
        Calls `download_complete()` when a download finishes.
        """
        with ProcessPoolExecutor(max_workers=self.processes) as executor:
            while self.queue:
                urls = pop_chunk(self.processes, self.queue.pop)
                self.visited |= set(urls)
                future_to_url = {executor.submit(download, url): url for url in urls}
                for f in as_completed(future_to_url, timeout=15):
                    self.download_complete(f, future_to_url[f])


def pop_chunk(n, fn):
    """ Calls fn() n-times, putting the return value in a list
    Args:
        n (int): maximum size of the chunk
        fn (func): function to call (probably some collection instance's pop() function)
    Returns:
        ([]) list of whatever items that were in 
    Example:
        >>> foo = [1, 2, 3, 4, 5]
        >>> pop_chunk(3, foo.pop)
        [5, 4, 3]
        >>> foo
        [1, 2]
    """
    return_values = []
    for _ in range(n):
        try:
            return_values.append(fn())
        except IndexError:
            break
    return return_values


def download(url):
    """ Uses 'downloader.py' to download a Web page's HTML content.
    Args:
        url (Url): The URL whose HTML we want to download/fetch
    Returns:
        (str) A string of the HTML content found at the given URL
    Note:
        This method is parallelized
    """
    abs_path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(abs_path, 'downloader.py')
    args = ['python', script_path, url.url]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    html = proc.stdout.read()
    return html.decode('utf-8')
