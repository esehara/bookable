# -*- coding: utf-8 -*-
from django.db import models


class BookLog(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u'最近クリックされた本'
        ordering = ['-updated_at']

    book = models.ForeignKey('shelf.Book', verbose_name=u'書籍')
    created_at = models.DateTimeField(u'作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(u'更新日時', auto_now=True)

    def __unicode__(self):
        return u"%s(%s)" % (self.book.title, self.updated_at)
