# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from apps.shelf.models import (Book, Keyword)


class Command(BaseCommand):

    def handle(self, *args, **opts):
        books = Book.objects.filter(for_random=None)
        for book in books:
            book.set_for_random()
            print "No.", book.pk
            print "for Random:", book.for_random

        keywords = Keyword.objects.filter(for_random=None)
        for keyword in keywords:
            keyword.set_for_random()
            print "Keyword:", keyword.name
            print "for Random", keyword.for_random
