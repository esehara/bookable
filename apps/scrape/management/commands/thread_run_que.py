# -*- coding:utf-8 -*-
import threading
from django.core.management.base import BaseCommand
from apps.scrape.management.commands.simple_run_que import AmazonLink
from apps.scrape.models import ScrapeQue
from apps.shelf.models import Book
from time import sleep


def amazon_process(my_que):
    global killall
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
                previous_bookcount = wait_commit(
                    book, bookcount, previous_bookcount)
        except IndexError:
            print "[Error] Index Error. %s is skip." % current_que
        except IOError:
            print "[Error] IO Error. %s is skip." % current_que
        if killall:
            break


def wait_commit(book, current, previous):
    while 1:
        if current != previous:
            break
        print "[Information][Child] Wait commit book about %s." % book
        print "[Information] Current: %d" % current
        print "[Information] Previous: %d" % previous
        sleep(2)
        book.save()
        current = Book.objects.all().count()
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

killall = False
class Command(BaseCommand):

    def handle(self, *args, **opts):
        global killall
        if len(args) == 0:
            thread_number = 3
        else:
            thread_number = int(args[0]) 
        max_que = thread_number * 100
        main_que = list(ScrapeQue.objects.filter(
            is_done=False)[0:max_que])
        child_ques = [[] for i in range(thread_number)]
        threads = generate_thread(child_ques)
        run_thread(threads)
        previous_bookcount = Book.objects.all().count()
        kill_counter = 0
        while 1:
            for que in child_ques:
                if len(que) == 0:
                    que.append(main_que.pop(0))

            if len(main_que) < max_que / 2:
                print "[Information][Main] Que is add."
                main_que += list(ScrapeQue.objects.filter(
                    is_done=False)[0:max_que / 2])

            print "[Information][Main] Rest Que is %d ." % len(main_que)
            sleep(60)
            current_bookcount = Book.objects.all().count()
            kill_counter += (current_bookcount == previous_bookcount)
            if kill_counter == 3:
                killall = True
                print "[Information] Kill all thread."
                sleep(5)
                child_ques = [[] for i in range(thread_number)]
                threads = generate_thread(child_ques)
                killall = False
                run_thread(threads)
            elif kill_counter > 0 and current_bookcount != previous_bookcount:
                kill_counter = 0
            previous_bookcount = current_bookcount
