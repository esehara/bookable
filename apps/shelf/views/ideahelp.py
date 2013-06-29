# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.shelf.models import Book


def index(request):
    page = request.GET.get('page', '1')
    d = Book.return_idea_dict()
    d['return_url'] += '?page=%s' % str(int(page) + 1)
    return render(
        request,
        'keyword.html',
        d)
