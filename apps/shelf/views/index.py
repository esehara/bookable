# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.shelf.models import Book


def index(request):
    page = request.GET.get('page', '1')
    page = int(page)
    d = Book.return_page_dict()
    d['return_url'] = '?page=%s' % str(int(page) + 1)
    d['page'] = page + 1
    return render(
        request,
        'index.html',
        d)
