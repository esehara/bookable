# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.shelf.models import Book


def index(request):
    page = request.GET.get('page', 1)
    d = Book.return_has_review_dict(page=int(page) - 1)
    d['return_url'] = 'latest?page=%d' % (int(page) + 1)
    return render(
        request,
        'review.html',
        d)
