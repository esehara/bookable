#-*- coding: utf-8 -*-
from django.db import models

class ScrapeQue(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u'Amazon情報習得Que'

    title = models.CharField(u'書名', max_length=255)
    url = models.URLField(u"Amazonへのリンク先")
    image = models.URLField(u"書影へのリンク", null=True)
    text = models.TextField(u"メモ", null=True)
    via = models.CharField(u"引用元", max_length=255)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(u'作成日時', auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.title
