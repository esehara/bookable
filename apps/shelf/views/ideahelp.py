# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.shelf.models import Book


def index(request):
    return render(
        request,
        'keyword.html',
        Book.return_idea_dict())
