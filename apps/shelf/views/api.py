# -*- coding: utf-8 -*-
from apps.shelf.models import Book
from django.http import HttpResponse


def book_random_api(request):
    return HttpResponse(
        Book.return_json_selialize(),
        mimetype='text/plain')
