# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import threading
import json
import urllib
import re
import redis
import time
from django.core.management.base import BaseCommand
from apps.scrape.models import ScrapeQue
from apps.scrape.management.commands import thread_run_que

url = ("http://b.hatena.ne.jp/entrylist"
       "?sort=count&url=http%3A%2F%2Fwww.amazon.co.jp%2F")


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
            self.image = None

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
        return re.sub(r'hatena-b-22/ref=nosim', '', self.link)

    def _fix_title(self, title):
        return re.sub(u'Amazon.co.jp： ', '', title)

    def _make_jsonable_dict(self):
        return {'users': self.users}

    def make_que(self):
        try:
            que = ScrapeQue.objects.get(
                url=self.fix_aff())
        except ScrapeQue.DoesNotExist:
            que = ScrapeQue.objects.create(
                title=self.title,
                url=self.fix_aff(),
                image=self.image,
                text=json.dumps(self._make_jsonable_dict()),
                via="HatenaBookMark")
            print u"No.%d: %s" % (que.pk, que.title)
        return que


def _get_links(pages):
    html = urllib.urlopen(url=url + "&of=" + str(pages * 20)).read()
    soup = BeautifulSoup(html)
    links = soup.find_all("li", {"class": "entry-unit"})
    return links


def factory_links(pages):
    links = _get_links(pages)
    return [HatenaBookmark(link) for link in links]


def hatebu_process(my_que, rs):
    while 1:
        if len(my_que) == 0:
            time.sleep(1)
            continue
        run_page = my_que.pop(0)
        print "Run Que --> Page: %d" % run_page
        _make_que(
            factory_links(run_page))
        rs.set('hatenabookmark-%d' % run_page, 'True')

class Command(BaseCommand):

    def handle(self, *args, **opts):
        rs = redis.Redis(host="127.0.0.1", port=6379, db=0)
        if len(args) == 0:
            pages = 0
        else:
            pages = int(args[0])

        if len(args) == 2:
            worker = int(args[1])
        else:
            worker = 10

        child_ques = [[] for i in range(worker)]
        threads = thread_run_que.generate_thread(
            child_ques, target=hatebu_process,
            thread_args=(rs,))
        thread_run_que.run_thread(threads)
        while 1:
            for que in child_ques:
                print "[Set Que] --> Page: %d" % pages
                print "[Result] -->", child_ques
                if (
                        len(que) == 0 and
                        rs.get('hatenabookmark-%s' % pages) == 'False'):
                    que.append(pages)
                pages += 1
                time.sleep(1)


def _make_que(links):
    for link in links:
        if link.is_book():
            link.make_que()
