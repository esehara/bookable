# -*- coding: utf-8 -*-
import re
import json
from django.test import TestCase
from apps.scrape.management.commands import hatebu
from apps.scrape.models import ScrapeQue

class HatenabookmarkScrapeTest(TestCase):
    
    debug_dict = {
            "title": u"テスト",
            "users": 2000,
            "link": "http://www.amazon.co.jp/exec/obidos/ASIN/4140814047/hatena-b-22/"}

    def test_get_link(self):
        u"""
        はてなブックマークからリンクを習得します。
        """
        links = hatebu._get_links(0)
        self.assertEqual(len(links), 20)

    def test_get_link_infomation(self):
        u"""
        はてなブックマークからリンクを習得し、
        その情報を格納します。
        """
        links = hatebu.factory_links(0)
        self.assertEqual(links[0].title, u'Amazon')
        self.assertTrue(int(links[0].users) > 1000)

    def test_fix_link_http(self):
        u"""
        はてなブックマークのリンクを習得し、
        そのリンク情報を修正します。
        """
        link = hatebu.HatenaBookmark(debug={
            "title": u"テスト",
            "users": 2000,
            "link": "/entry/www.amazon.co.jp/"})
        link.link = link._fix_link(link.link)
        self.assertEqual(link.link, u'http://www.amazon.co.jp/')

    def test_it_is_goodslink(self):
        u"""
        習得したリンクが商品へのリンクかどうかを
        判定します。
        """
        link = hatebu.HatenaBookmark(debug={
            "title": u"テスト",
            "users": 2000,
            "link": "http://www.amazon.co.jp/"})
        self.assertFalse(link.is_book())

        link = hatebu.HatenaBookmark(debug={
            "title": u"テスト",
            "users": 2000,
            "link": "http://www.amazon.co.jp/exec/obidos/ASIN/4140814047/hatena-b-22/"})
        self.assertTrue(link.is_book())

    def test_fix_aff_id(self):
        u"""
        アフィリエイトのIDを入れ替えます
        """
        link = hatebu.HatenaBookmark(
            debug=self.debug_dict)
        link.link = link.fix_aff()
        self.assertFalse(
            re.search('hatebu-22', link.link))

    def test_title_fix(self):
        link = hatebu.HatenaBookmark(
            debug={
                "title": u"Amazon.co.jp： フリー~〈無料〉からお金を生み出す新戦略",
                "users": 2000,
                "link": "hoge"})
        self.assertFalse(
            re.search('Amazon.co.jp', link._fix_title(link.title)))

    def test_generate_que(self):
        link = hatebu.HatenaBookmark(debug=self.debug_dict)
        link.make_que()
        que = ScrapeQue.objects.get(url=link.fix_aff())
        option = json.loads(que.text)
        self.assertEqual(option['users'], 2000)

    def test_generate_que_not_dublicate(self):
        link = hatebu.HatenaBookmark(debug=self.debug_dict)
        link.make_que()
        link.make_que()
        que = ScrapeQue.objects.get(url=link.fix_aff())
        self.assertTrue(que)

from apps.scrape.management.commands import run_que
from apps.shelf.models import Book


class GetAmazonDataTest(TestCase):

    def setUp(self):
        debug_dict = {
            "title": u"テスト",
            "users": 2000,
            "link": "http://www.amazon.co.jp/exec/obidos/ASIN/4140814047/hatena-b-22/"}
        link = hatebu.HatenaBookmark(debug=debug_dict)
        link.make_que()
        self.test_que = ScrapeQue.objects.filter(is_done=False)[0]

    def test_get_amazonlink(self):
        amazon = run_que.AmazonLink(self.test_que)
        self.assertEqual(
            amazon.title,
            u'フリー~〈無料〉からお金を生みだす新戦略')

    def test_model_save(self):
        amazon = run_que.AmazonLink(self.test_que)
        amazon.save()
        book = Book.objects.all()[0]
        self.assertEqual(amazon.title, book.title)
        self.assertEqual(book.users, 2000)

    def test_que_is_done(self):
        amazon = run_que.AmazonLink(
            self.test_que)
        amazon.save()
        self.assertTrue(self.test_que.is_done)
