# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re

url = "http://b.hatena.ne.jp/entrylist?sort=count&url=http%3A%2F%2Fwww.amazon.co.jp%2F"

class HatenaBookmark(object):
    def __init__(self, soup_element=None, debug=None):
        if debug is None:
            self._link_tag = self._find_link_tag(soup_element)
            self._raw_link = self._link_tag.get('href')
            self.title = self._fix_title(
                self._link_tag.get('title'))
            self.users = self._find_users(soup_element)
            self.link = self._fix_link(self._raw_link)
            self.image = self._find_image(soup_element)
        else:
            self.title = debug['title']
            self.users = debug['users']
            self.link = debug['link']

    def _find_link_tag(self, soup_element):
        return soup_element.find('a', {"class": "entry-link"})

    def _find_users(self, soup_element):
        return soup_element.find('span').text

    def _find_image(self, soup_element):
        return soup_element.find('img').get('src')

    def _fix_link(self, link):
        return re.sub(r'^/entry/', 'http://', link)

    def is_book(self):
        return re.search('exec/obidos/ASIN/', self.link)

    def fix_aff(self):
        return re.sub(r'hatena-b-22', 'bookable052e-22', self.link)

    def _fix_title(self, title):
        return re.sub(u'Amazon.co.jp： ', '', title)


def _get_links(pages):
    html = urllib.urlopen(url=url + "&of=" + str(pages * 20)).read()
    soup = BeautifulSoup(html)
    links = soup.find_all("li", {"class": "entry-unit"})
    return links

def factory_links(pages):
    links = _get_links(pages)
    return [HatenaBookmark(link) for link in links]
