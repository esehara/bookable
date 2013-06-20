# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from apps.shelf.models import Book


class Command(BaseCommand):

    def handle(self, *args, **opts):
        print '"Users","Books", "Average Price"'
        for users in range(264):
            get_users = 264 - users
            user_number = Book.objects.filter(users=get_users).count()
            sum_price = 0
            average = 0
            for book in Book.objects.filter(users=get_users):
                if book.price == 0:
                    continue
                sum_price += book.price
            if sum_price is not 0:
                average = sum_price / Book.objects.filter(users=get_users, price__gt=0).count()
            print '%d, %d, %d' % (
                get_users,
                user_number,
                average)
