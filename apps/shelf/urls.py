# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url('^$',
        'apps.shelf.views.index.index',
        name='index'),

    url('keyword',
        'apps.shelf.views.keyword.index',
        name='keyword'),

    url('^api/books/random$',
        'apps.shelf.views.api.book_random_api',
        name='get_random_books_api')
)
