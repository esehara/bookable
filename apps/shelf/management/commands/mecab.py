# -*- coding: utf-8 -*-
import MeCab
from django.core.management.base import BaseCommand
from apps.shelf.models import (
    Keyword, KeywordToBook, Book)
# define mecab dictionary
mecab = MeCab.Tagger("mecabrc")


class MecabToken(object):

    def __init__(self, node, model=None):
        self._generate_text(node.surface)
        self._generate_type_and_subtype(node.feature)
        self.model = model

    def _generate_text(self, node_surface):
        if isinstance(node_surface, str):
            node_surface = node_surface.decode('utf-8')
        self.text = node_surface

    def _generate_type_and_subtype(self, node_feature):
        if isinstance(node_feature, str):
            node_feature = node_feature.decode('utf-8')
        feature_array = node_feature.split(u',')
        self.type = feature_array[0]
        self.subtype = feature_array[1]

    def is_noun(self):
        return (
            self.type == u"名詞" and self.subtype != u"代名詞")


class MecabManager(object):

    def __init__(self, bookmodel=None, debug=None):
        self.tokens = []
        self.model = None
        if debug is not None:
            initialize = debug['title']
            if bookmodel is not None:
                self.model = bookmodel
        else:
            initialize = bookmodel.title
            self.model = bookmodel
        self._mecab_initialize(initialize)

    def _mecab_initialize(self, text):

        if isinstance(text, unicode):
            text = text.encode('utf-8')
        self._node = mecab.parseToNode(text)
        self._mecab_analyze()

    def _mecab_analyze(self):
        node = self._node
        while node:
            if node.surface == "":
                node = node.next
                continue
            self.tokens.append(MecabToken(node, model=self.model))
            node = node.next

    def _create_keyword(self):
        for num, token in enumerate(self.tokens):
            self.tokens[num].keyword_model = None
            if token.is_noun():
                try:
                    keyword = Keyword.objects.get(
                        name=token.text)
                    keyword.times += 1
                    model = keyword.save()
                    self.tokens[num].keyword_model = model
                except Keyword.DoesNotExist:
                    keyword = Keyword.objects.create(
                        name=token.text)
                    self.tokens[num].keyword_model = keyword
                finally:
                    print keyword

    def create_keyword_to_book(self):
        self._create_keyword()
        ktb = None
        for token in self.tokens:
            
            if token.keyword_model is None:
                continue
            try:
                ktb = KeywordToBook.objects.get(
                    book=token.model,
                    keyword=token.keyword_model)
            except KeywordToBook.DoesNotExist:
                ktb = KeywordToBook.objects.create(
                    book=token.model,
                    keyword=token.keyword_model)
            finally:
                print ktb

        self.model.is_mecab = True
        self.model.save()


class Command(BaseCommand):

    def handle(self, *args, **opts):
        while 1:
            book = Book.objects.filter(is_mecab=False)[0]
            if book.title != "":
                print "[Books]: %s" % (book)
                mecabm = MecabManager(book)
                mecabm.create_keyword_to_book()
            else:
                print "PASS"
                book.is_mecab = True
                book.save()
