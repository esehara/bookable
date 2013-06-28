# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.utils.http import urlencode
from apps.shelf.models import Keyword


def index(request):
    page = request.GET.get('page', 1)
    keyword = request.GET.get('query', None)
    d = Keyword.return_page_search_dict(
        page=int(page) - 1, keyword=keyword)
    d['return_url'] = "search?" + urlencode(
        [('page', int(page) + 1)]) + "&" + urlencode(
            [('query', keyword)])
    return render(
        request,
        'search.html',
        d)
