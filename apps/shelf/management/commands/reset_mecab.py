# -*- coding: utf-8 -*

from django.core.management.base import BaseCommand
from apps.shelf.models import Keyword, KeywordToBook, Book


class Command(BaseCommand):

    def handle(self, *args, **opts):
        print "[Delete Keyword Model]"
        Keyword.objects.all().delete()
        print "[Delete KeywordToBook]"
        KeywordToBook.objects.all().delete()
        print "[Return Book status]"
        Book.objects.update(is_mecab=False)
