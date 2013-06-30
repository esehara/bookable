# -*- coding:utf-8 -*-
import threading
from django.core.management.base import BaseCommand
from apps.scrape.management.commands.simple_run_que import AmazonLink
from apps.scrape.models import ScrapeQue
from apps.shelf.models import Book
from time import sleep


def amazon_process(my_que):
    previous_bookcount = 0
    while 1:
        if len(my_que) == 0:
            "[Thread] Wait Job..."
            sleep(1)
            continue
        current_que = my_que.pop(0)
        try:
            amazon = AmazonLink(current_que)
            book = amazon.save()
            if book is not None:
                book.save()
                bookcount = print_book(book)
                previous_bookcount = wait_commit(book, bookcount, previous_bookcount)
        except IndexError:
            print "[Error] Index Error. %s is skip." % current_que
        except IOError:
            print "[Error] IO Error. %s is skip." % current_que


def wait_commit(book, current, previous):
    while 1:
        if current != previous:
            break
        sleep(1)
        current = Book.objects.all().count()
    book.save()
    return current


def print_book(book):
    if book is not None:
        bookcount = Book.objects.all().count()
        print bookcount, u'冊目'
        print "[Infomation] %s %s" % (book.title, book.author)
    else:
        print "[Failed] cannot get book infomation."
    print

    return bookcount


def generate_thread(
        common_array,
        target=amazon_process,
        thread_args=()):
    result_thread = []

    for number, arr in enumerate(common_array):
        th = threading.Thread(
            target=target,
            args=(arr, ) + thread_args,
            name="thread%d" % number)
        th.que = arr
        th.setDaemon(True)
        result_thread.append(th)
    return result_thread


def run_thread(threads):
    for thread in threads:
        thread.start()

class Command(BaseCommand):

    def handle(self, *args, **opts):

        if len(args) == 0:
            thread_number = 3
        else:
            thread_number = int(args[0]) 
        child_ques = [[] for i in range(thread_number)]
        max_que = thread_number * 100
        main_que = list(ScrapeQue.objects.filter(
            is_done=False)[0:max_que])
        threads = generate_thread(child_ques)
        run_thread(threads)
        while 1:
            for que in child_ques:
                if len(que) == 0:
                    que.append(main_que.pop(0))

            if len(main_que) < max_que / 2:
                main_que += list(ScrapeQue.objects.filter(
                    is_done=False)[0:max_que / 2])

            print "[Infomation][Main] Rest Que is %d ." % len(main_que)
            sleep(5)
