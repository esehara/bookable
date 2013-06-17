# -*- coding:utf-8 -*-
import urllib
import re
import json
from bs4 import BeautifulSoup
from apps.shelf.models import Book
from apps.scrape.models import ScrapeQue
from django.core.management.base import BaseCommand


class AmazonLink(object):

    def __init__(self, que):
        self._que = que
        self._get_bookdata()

    def _get_html(self):
        html = urllib.urlopen(self._que.url)
        self._raw_html = html.read()
        self.response = html.getcode()
        return BeautifulSoup(self._raw_html)

    def _get_bookdata(self):
        soup = self._get_html()
        print self._que.url
        if self.response != 404:
            if (
                    soup.center and
                    u'アダルト商品' in self._raw_html.decode('cp932')):
                self.response = 404
                return

            if (
                    soup.find('span', {'class': 'h1'}) and
                    u'18歳未満' in self._raw_html.decode('cp932')):
                self.response = 404
                return

            self.title = re.sub(
                r'\[.*\]', '', soup.h1.text).replace(u'\n', '').strip()
            div_all = soup.find_all('div', {'class': 'buying'})
            div = None
            for elem in div_all:
                if not 'amznJQ' in elem.text:
                    div = elem.text
                    break

            if div is None:
                self.response = 404
                return
            self.author = div.split(soup.h1.text)[-1].strip()

            if len(self.author) > 250:
                self.author = self.author[:250] + u'…‥'
            
            try:
                if soup.find('b', {'class': 'priceLarge'}):
                    self.price = int(soup.find(
                        'b', {'class': 'priceLarge'}).text.replace(
                            u',', u'').replace(u'￥', u''))
                else:
                    self.price = 0
            except UnicodeEncodeError:
                self.price = 0
            except ValueError:
                self.price = 0

            self.detail = str(soup.find(
                'div', {'class': 'productDescriptionWrapper'}))

    def save(self):
        option_data = json.loads(self._que.text)

        if self.response == 404:
            self._que.is_done = True
            self._que.save()
            return None

        try:
            book = Book.objects.get(url=self._que.url)
        except Book.DoesNotExist:
            book = Book.objects.create(
                title=self.title,
                author=self.author,
                price=self.price,
                url=self._que.url,
                image=self._que.image,
                detail=self.detail,
                users=int(option_data['users']),
                via=u'はてなブックマーク')
        self._que.is_done = True
        self._que.save()
        return book


class Command(BaseCommand):

    def handle(self, *args, **opts):
        while 1:
            try:
                que = ScrapeQue.objects.filter(
                    is_done=False)[0]
                amazon = AmazonLink(que)
                book = amazon.save()
                if book is not None:
                    print "[ BOOK ]"
                    print book.title
                    print book.author
                    print book.price, u'円'
                else:
                    print "-- Pass --"
            except IndexError:
                continue
            except IOError:
                continue
