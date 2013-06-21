# -*- coding: utf-8 -*-
import MeCab
from apps.shelf.models import Keyword
# define mecab dictionary
mecab = MeCab.Tagger("mecabrc")


class MecabToken(object):

    def __init__(self, node):
        self._generate_text(node.surface)
        self._generate_type_and_subtype(node.feature)

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
        if debug is not None:
            initialize = debug['title']
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
            self.tokens.append(MecabToken(node))
            node = node.next

    def _create_keyword(self):
        for token in self.tokens:
            if token.is_noun():
                try:
                    keyword = Keyword.objects.get(
                        name=token.text)
                    keyword.times += 1
                    model = keyword.save()
                    token.model = model
                except Keyword.DoesNotExist:
                    model = Keyword.objects.create(
                        name=token.text)
                    token.model = model
