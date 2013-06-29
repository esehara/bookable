# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.cache import cache
from apps.booklog.models import BookLog


def latest(request):
    page = request.GET.get('page', '1')
    cache_key = 'latest_cache_dict_page_%s' % page
    cache_time = 600

    d = cache.get(cache_key)
    if not d:
        d = BookLog.return_page_click_dict(page=int(page) - 1)
        cache.set(cache_key, d, cache_time)

    d['return_url'] = "latest?page=%d" % (int(page) + 1)
    d['page'] = int(page) + 1
    return render(
        request,
        'latest.html',
        d)
