# -*- coding: utf-8 -*-
import re
from django.test import TestCase
from apps.scrape.management.commands import hatebu

class HatenabookmarkScrapeTest(TestCase):

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
            debug={
                "title": u"テスト",
                "users": 2000,
                "link": "http://www.amazon.co.jp/exec/obidos/ASIN/4140814047/hatena-b-22/"})
        link.link = link.fix_aff()
        self.assertTrue(
            re.search('bookable052e-22', link.link))

    def test_title_fix(self):
        link = hatebu.HatenaBookmark(
            debug={
                "title": u"Amazon.co.jp： フリー~〈無料〉からお金を生み出す新戦略",
                "users": 2000,
                "link": "hoge"})
        self.assertFalse(
            re.search('Amazon.co.jp', link._fix_title(link.title)))
