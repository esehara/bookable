# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url('^latest$',
        'apps.booklog.views.latest',
        name='latest'),

)
