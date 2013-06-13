# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.shelf.models import Book


def index(request):
    return render(
        request,
        'index.html',
        Book.return_page_dict())
