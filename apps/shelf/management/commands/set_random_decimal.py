# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from apps.shelf.models import Book


class Command(BaseCommand):

    def handle(self, *args, **opts):
        books = Book.objects.filter(for_random=None)
        for book in books:
            book.set_for_random()
            print "No.", book.pk
            print "for Random:", book.for_random
