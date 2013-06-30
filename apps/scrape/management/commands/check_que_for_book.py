# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from apps.scrape.models import ScrapeQue
from apps.shelf.models import Book


def check_another_url(que):
    try:
        book = Book.objects.get(url=que.url.replace(
            'bookable052e-22/ref=nosim', ''))
        que.url = book.url
        que.is_done = True
        que.save()
    except Book.DoesNotExist:
        print "Que No. %d is None." % que.pk
        print que
        print que.url
        que.is_done = False
        que.save()

class Command(BaseCommand):

    def handle(self, *args, **orpts):
        ques = ScrapeQue.objects.filter(is_done=True)
        for que in ques:
            print "Check Que No. %d." % que.pk
            try:
                Book.objects.get(url=que.url)
            except Book.DoesNotExist:
                check_another_url(que)
