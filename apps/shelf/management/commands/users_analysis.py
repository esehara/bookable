# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from apps.shelf.models import Book


class Command(BaseCommand):

    def handle(self, *args, **opts):
        print "Analize Book Users"
        for users in range(264):
            get_users = 264 - users
            print "%d %d" % (
                get_users,
                Book.objects.filter(users=get_users).count())
