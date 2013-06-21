# -*- coding: utf-8 -*-
import MeCab
from django.test import TestCase
from apps.shelf.management.commands.mecab import (
    MecabManager, MecabToken)
from apps.shelf.models import Book, Keyword

class MecabTokenTest(TestCase):
    def setUp(self):
        mecab = MeCab.Tagger("mecabrc")

        # initialize
        mecab.parseToNode('initialize')

        self._testnode = mecab.parseToNode(
            'これはテストデータです')
        self._generate_valid_token()

    def _generate_valid_token(self):
        node = self._testnode
        while node:
            if node.surface == "":
                node = node.next
                continue
            self.valid_node_token = MecabToken(node)
            break

    def test_mecab_tokenize(self):
        self.assertEqual(
            self.valid_node_token.text, u'これ')

    def test_mecab_get_wordtype(self):
        self.assertEqual(
            self.valid_node_token.type, u'名詞')
        self.assertEqual(
            self.valid_node_token.subtype, u'代名詞')


class MecabTest(TestCase):

    def setUp(self):
        self.debug = {
            'title': u"これはテストデータです"}
        self.mecabm = MecabManager(
            debug=self.debug)

    def test_mecab_initialize(self):
        u"""
        Mecabを使えるように設定します
        """
        self.assertTrue(self.mecabm._node)

    def test_mecab_tokenize(self):
        u"""
        Mecabのnodeからトークンを生成します
        """
        self.assertTrue(
            len(self.mecabm.tokens) > 0)
        self.assertEqual(
            self.mecabm.tokens[0].text, u'これ')

    def assertNoun(self, token, text, is_noun):
        self.assertEqual(token.text, text)
        if is_noun:
            self.assertTrue(token.is_noun())
        else:
            self.assertFalse(token.is_noun())

    def test_mecab_noun_check(self):
        u"""
        名詞かどうかチェックします
        """
        tokens = self.mecabm.tokens
        self.assertNoun(tokens[0], u'これ', False)
        self.assertNoun(tokens[1], u'は', False)
        self.assertNoun(tokens[2], u'テスト', True)

    def generate_book(self):
        return Book.objects.create(
            title=u'これはテストです',
            author=u'これは著者です',
            price=1000,
            url='http://',
            image='http://',
            detail=u'これはテスト詳細です',
            users=300,
            is_mecab=False,
            via=u'はてなブックマーク')

    def generate_mecab_model(self):
        self.mecabm = MecabManager(
            bookmodel=self.generate_book())

    def test_mecab_book_tokenlize(self):
        self.generate_mecab_model()
        tokens = self.mecabm.tokens
        self.assertNoun(tokens[0], u'これ', False)
        self.assertNoun(tokens[2], u'テスト', True)

    def test_token_to_model(self):
        self.generate_mecab_model()
        self.mecabm._create_keyword()
        keyword = Keyword.objects.get(
            name=u'テスト')
        self.assertEqual(keyword.name, u'テスト')

        is_not_noun = False
        try:
            keyword = Keyword.objects.get(
                name=u'これ')
        except Keyword.DoesNotExist:
            is_not_noun = True
        self.assertTrue(is_not_noun)


class BookModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title=u'これはテストです',
            author=u'これは著者です',
            price=1000,
            url=u'http://www.amazon.co.jp/exec/obidos/ASIN/4140814047/',
            image='http://',
            detail=u'これはテスト詳細です',
            users=300,
            is_mecab=False,
            via=u'はてなブックマーク')

    def test_url_to_bookmark(self):
        self.assertEqual(
            u'http://b.hatena.ne.jp/entry/www.amazon.co.jp/gp/product/4140814047/',
            self.book.link_to_hatenabookmark())
