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

    @classmethod
    def return_page_click_dict(cls, page=0):
        d = {
            'kfirst': [],
            'ksecond': [],
            'kthird': [],
            'kforth': [],
            'autopage': True}

        booklog = list(BookLog.objects.all()[page * 20:(page + 1) * 20])
        if BookLog.objects.all().count() < (page + 1) * 20:
            d['autopage'] = False

        for num, log in enumerate(booklog):
            push_column = lambda x: num % 4 == x
            if push_column(0):
                d['kfirst'].append(log.book)
            if push_column(1):
                d['ksecond'].append(log.book)
            elif push_column(2):
                d['kthird'].append(log.book)
            elif push_column(3):
                d['kforth'].append(log.book)
        return d
