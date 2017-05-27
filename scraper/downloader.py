""" Module to download the HTML of a dynamic or static Web site.

Uses PyQt to access the Qt GUI framework.
This uses the C++ bindings to access Webkit browser that
we can use to fully render a Web page before parsing its HTML.

# Example Usage
`see code at bottom`
"""
import argparse
from sys import platform

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class WebkitRenderer(QWebEnginePage):
    """ Class to render a given URL """

    def __init__(self, rendered_callback):
        """
        Args:
            rendered_callback (func): called once a Web page is rendered.

        Callback Args:
            url (str): The URL of the Web page.
            html (str): HTML of the rendered Web page.
        """
        self.app = QApplication([])
        super(WebkitRenderer, self).__init__()
        self.loadFinished.connect(self._loadFinished)
        self.rendered_callback = rendered_callback

    def javaScriptConsoleMessage(self, msg_level, p_str, p_int, p_str_1):
        """ Ignore console messages """
        pass

    def render(self, url):
        """ Download and render the URL
        Args:
            url (str): The URL to load.
        """
        self.load(QUrl(url))
        self.app.exec()  # put app into infinite loop, listening to signals/events

    def _loadFinished(self, result):
        """ Event handler - A Web page finished loading
        Args:
            result (bool): success indicator
        """
        if result:
            self.toHtml(self.html_callback)  # async and takes a callback
        else:
            url = self.url().toString()
            self.rendered_callback(url, None)
            self.app.quit()

    def html_callback(self, data):
        """ Receives rendered Web Page's HTML """
        url = self.url().toString()
        self.rendered_callback(url, data)
        self.app.quit()  # break app out of infinite loop


if __name__ == '__main__':

    if platform == 'darwin':  # if mac: hide python launch icons
        import AppKit
        info = AppKit.NSBundle.mainBundle().infoDictionary()
        info["LSBackgroundOnly"] = "1"
    # render_engine.py needs to be able to run as a
    # standalone script to achieve parallelization.
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    args = parser.parse_args()

    def cb(url, html):
        print(html)

    wr = WebkitRenderer(cb)
    wr.render(args.url)
