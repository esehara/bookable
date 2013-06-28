# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url('^$',
        'apps.shelf.views.index.index',
        name='index'),

    url('^keyword$',
        'apps.shelf.views.keyword.index',
        name='keyword'),

    url('^keyword/list$',
        'apps.shelf.views.keyword.list',
        name='keyword-list'),

    url('^search$',
        'apps.shelf.views.search.index',
        name='search'),

    url('^idea$',
        'apps.shelf.views.ideahelp.index',
        name='ideahelp'),

    url('book/(?P<model_id>\d+)$',
        'apps.shelf.views.book.to_amazon',
        name='amazon-redirect'),

    url('^review$',
        'apps.shelf.views.review.index',
        name='review'),

    url('^api/books/random$',
        'apps.shelf.views.api.book_random_api',
        name='get_random_books_api')
)
