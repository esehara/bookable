# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.cache import cache
from apps.shelf.models import Book


def index(request):
    page = request.GET.get('page', '1')
    
    cache_key = 'index_cache_dict_page_%s' % page
    cache_time = 180
    d = cache.get(cache_key)

    if not d:
        d = Book.return_page_dict()
        cache.set(cache_key, d, cache_time)

    d['return_url'] = '?page=%s' % str(int(page) + 1)
    return render(
        request,
        'index.html',
        d)
