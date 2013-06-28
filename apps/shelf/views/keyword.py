#-*- coding: utf-8 -*-
from django.shortcuts import render
from apps.shelf.models import Book, Keyword


def index(request):
    return render(
        request,
        'keyword.html',
        Book.return_keyword_dict())


def list(request):
    return render(
        request,
        'keyword_list.html',
        Keyword.return_keyword_dict())
