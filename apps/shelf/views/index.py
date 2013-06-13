# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.shelf.models import Book


def index(request):
    d = {}
    d['favorite_books'] = Book.objects.filter(
        users__gt=100).order_by('?')[:2]
    d['normal_books'] = Book.objects.filter(
        users__lt=100, users__gt=50).order_by('?')[:2]
    d['newbee_books'] = Book.objects.filter(
        users__lt=50).order_by('?')[:2]
    return render(
        request, 'index.html', d)
