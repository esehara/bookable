# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url('^$',
        'apps.shelf.views.index.index',
        name='index'),)
