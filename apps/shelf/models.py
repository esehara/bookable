# -*- coding:utf-8 -*-
from django.db import models
from django.core.serializers import serialize
from django.conf import settings


class Book(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"書誌情報"
        ordering = ['-click']

    title = models.CharField(u'書名', max_length=255)
    author = models.CharField(u'著者', max_length=255)
    price = models.IntegerField(u'値段')
    url = models.URLField(u'Amazonへのリンク先', db_index=True)
    image = models.URLField(u'書影へのリンク', null=True)
    detail = models.TextField(u'書誌詳細情報')
    users = models.IntegerField(u'はてなブックマークユーザー数', null=True, db_index=True)
    is_mecab = models.BooleanField(u'Mecab解析', default=False)
    text = models.TextField(u'紹介文章', null=True)
    via = models.CharField('引用元', max_length=255)
    click = models.IntegerField(u'クリック数', default=0)
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
                users__lt=max_users, users__gt=min_users).order_by('?')[:get])

    @classmethod
    def return_page_dict(cls):
        d = {}
        d['favorite_books'] = list(cls.objects.filter(users__gt=25).order_by('?')[:5])
        d['normal_books'] = Book.return_books(
            min_users=10, max_users=25)
        d['hot_books'] = Book.return_books(
            min_users=5, max_users=10)
        d['newbee_books'] = list(cls.objects.filter(users__lt=5).order_by('?')[:5])
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
        d['ds'].append(_get_keyword())
        d['return_url'] = 'keyword'
        return d

    @classmethod
    def return_idea_dict(cls):
        d = {'ds': []}
        for i in range(5):
            d['ds'].append(
                _get_keyword(
                    get_books=1, limit=1))
        d['return_url'] = 'idea'
        return d

    @classmethod
    def return_has_review_dict(cls, page=0):
        d = {
            'kfirst': [],
            'ksecond': [],
            'kthird': [],
            'kforth': [],
            'autopage': True}

        books = list(
            Book.objects.all().exclude(
                text=None).order_by('-created_at')[page * 20:(page + 1) * 20])
        if Book.objects.all().exclude(text=None).count() < (page + 1) * 20:
            d['autopage'] = False

        for num, book in enumerate(books):
            push_column = lambda x: num % 4 == x
            if push_column(0):
                d['kfirst'].append(book)
            if push_column(1):
                d['ksecond'].append(book)
            elif push_column(2):
                d['kthird'].append(book)
            elif push_column(3):
                d['kforth'].append(book)
        return d 

def _get_keyword(get_books=3, limit=5):

    class Wrapper:

        def __init__(self, keyword):
            self.keyword = keyword

        def get_books(self):
            self.books = [
                i.book for i in
                list(KeywordToBook.objects.filter(
                    keyword=self.keyword).order_by('?')[:get_books])]
    _d = {}
    if limit > 1:
        keywords = list(
            Keyword.objects.filter(times__gt=limit).order_by('?')[:5])
    else:
        keywords = list(
            Keyword.objects.order_by('?')[:5])

    for tkey in ['kfirst', 'ksecond', 'kthird', 'kforth']:
        _d[tkey] = Wrapper(keywords.pop(0))
        _d[tkey].get_books()

    return _d


class Keyword(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"キーワード"
        ordering = ['-times']
    name = models.CharField(u'キーワード', max_length=255)
    times = models.IntegerField(u'頻度', default=1)
    text = models.TextField(u'解説', null=True, blank=True)
    created_at = models.DateTimeField(u'作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(u'更新日時', auto_now=True)

    def __unicode__(self):
        return u"%s" % self.name
 
    @classmethod
    def return_keyword_dict(cls):
        d = {
            'kfirst': [],
            'ksecond': [],
            'kthird': [],
            'kforth': [],
            'return_url': 'keyword/list'}

        keywords = list(
            Keyword.objects.filter(times__gt=20).order_by('?')[:20])

        for num, keyword in enumerate(keywords):
            push_column = lambda x: num % 4 == x
            if push_column(0):
                d['kfirst'].append(keyword)
            if push_column(1):
                d['ksecond'].append(keyword)
            elif push_column(2):
                d['kthird'].append(keyword)
            elif push_column(3):
                d['kforth'].append(keyword)
        return d 

    @classmethod
    def return_page_search_dict(cls, page=0, keyword=None):
        d = {
            'kfirst': [],
            'ksecond': [],
            'kthird': [],
            'kforth': [],
            'autopage': True}

        if keyword is None:
            keyword = Keyword.objects.order_by('?')[0]
        else:
            try:
                keyword = Keyword.objects.get(name=keyword)
            except Keyword.DoesNotExist:
                keyword = Keyword.objects.order_by('?')[0]

        ktbs = list(
            KeywordToBook.objects.filter(
                keyword=keyword)[page * 20:(page + 1) * 20])

        if KeywordToBook.objects.filter(
                keyword=keyword).count() < (page + 1) * 20:
            d['autopage'] = False
        d['keyword'] = keyword
        randbook = KeywordToBook.objects.filter(
            keyword=keyword).order_by('?')[0].book
        d['nextkeyword'] = KeywordToBook.objects.exclude(keyword=keyword).filter(
            book=randbook).order_by('?')[0].keyword
        for num, ktb in enumerate(ktbs):
            push_column = lambda x: num % 4 == x
            if push_column(0):
                d['kfirst'].append(ktb.book)
            if push_column(1):
                d['ksecond'].append(ktb.book)
            elif push_column(2):
                d['kthird'].append(ktb.book)
            elif push_column(3):
                d['kforth'].append(ktb.book)
        return d

class KeywordToBook(models.Model):

    keyword = models.ForeignKey(
        Keyword,
        verbose_name=u'キーワード',
        db_index=True)
    book = models.ForeignKey(
        Book,
        verbose_name=u'書籍',
        db_index=True)

    def __unicode__(self):
        return u"%s -> %s" % (
            self.keyword.name, self.book.title)
