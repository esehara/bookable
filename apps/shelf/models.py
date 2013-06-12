# -*- coding:utf-8 -*-
from django.db import models


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


class Keyword(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"キーワード"

    name = models.CharField(u'キーワード', max_length=255)
    text = models.TextField(u'解説')
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
