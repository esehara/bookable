# -*- coding:utf-8 -*-
from django.db import models
from django.core.serializers import serialize
from django.conf import settings


class Book(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"書誌情報"
        ordering = ['created_at']

    title = models.CharField(u'書名', max_length=255)
    author = models.CharField(u'著者', max_length=255)
    price = models.IntegerField(u'値段')
    url = models.URLField(u'Amazonへのリンク先')
    image = models.URLField(u'書影へのリンク', null=True)
    detail = models.TextField(u'書誌詳細情報')
    users = models.IntegerField(u'はてなブックマークユーザー数', null=True)
    is_mecab = models.BooleanField(u'Mecab解析', default=False)
    text = models.TextField(u'紹介文章', null=True)
    via = models.CharField('引用元', max_length=255)
    created_at = models.DateTimeField(u'作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(u'更新日時', auto_now=True)

    def __unicode__(self):
        return u"%s %s" % (self.title, self.author)

    def affilize(self):
        return u"%s%s/" % (self.url, settings.AMAZON_ID)

    def link_to_hatenabookmark(self):
        link = self.url
        link = link.replace('http://', 'http://b.hatena.ne.jp/entry/')
        link = link.replace('/exec/obidos/ASIN/', '/gp/product/')
        return link

    @classmethod
    def return_books(cls, get=5, min_users=0, max_users=10000):
        return list(
            cls.objects.filter(
                users__gt=min_users, users__lt=max_users).order_by('?')[:get])

    @classmethod
    def return_page_dict(cls):
        d = {}
        d['favorite_books'] = Book.return_books(min_users=25)
        d['normal_books'] = Book.return_books(
            min_users=10, max_users=25)
        d['hot_books'] = Book.return_books(
            min_users=5, max_users=10)
        d['newbee_books'] = Book.return_books(max_users=5)
        return d

    @classmethod
    def return_json_selialize(cls):
        d = cls.return_page_dict()
        return u"""
{"favorite_books": %s,
 "normal_books": %s,
 "hot_books": %s,
 "newbee_books": %s}
        """ % (
            serialize('json', d['favorite_books']),
            serialize('json', d['normal_books']),
            serialize('json', d['hot_books']),
            serialize('json', d['newbee_books']))

    @classmethod
    def return_keyword_dict(cls):

        d = {'ds': []}

        class FourColumn:
            def __init__(self, pre_list):
                self.kfirst = pre_list.pop(0)
                self.kfirst.books = [self.kfirst]
                self.ksecond = pre_list.pop(0)
                self.ksecond.books = [self.ksecond]
                self.kthird = pre_list.pop(0)
                self.kthird.books = [self.kthird]
                self.kforth = pre_list.pop(0)
                self.kforth.books = [self.kforth]

        pre_list = list(KeywordToBook.objects.order_by('?')[:20])

        while pre_list:
            print pre_list
            d['ds'].append(FourColumn(pre_list))

        return d


class Keyword(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"キーワード"

    name = models.CharField(u'キーワード', max_length=255)
    times = models.IntegerField(u'頻度', default=1)
    text = models.TextField(u'解説', null=True, blank=True)
    created_at = models.DateTimeField(u'作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(u'更新日時', auto_now=True)

    def __unicode__(self):
        return u"%s" % self.name


class KeywordToBook(models.Model):

    keyword = models.ForeignKey(Keyword, verbose_name=u'キーワード')
    book = models.ForeignKey(Book, verbose_name=u'書籍')

    def __unicode__(self):
        return u"%s -> %s" % (
            self.keyword.name, self.book.title)
