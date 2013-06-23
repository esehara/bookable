#-*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404
from apps.shelf.models import Book
from apps.booklog.models import BookLog


def to_amazon(request, model_id):
    book = get_object_or_404(Book, pk=model_id)
    book.click += 1
    book.save()
    try:
        booklog = BookLog.objects.get(book=book)
        booklog.save()
    except BookLog.DoesNotExist:
        BookLog.objects.create(book=book)
    return redirect(book.affilize())
