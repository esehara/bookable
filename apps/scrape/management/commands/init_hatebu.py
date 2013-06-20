# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import redis

class Command(BaseCommand):
    
    def handle(self, *args, **opts):
        if len(args) == 0:
            pages = 0
        else:
            pages = int(args[0])
        rs = redis.Redis(host='127.0.0.1', port=6379, db=0)
        for page in range(10000, 20000):
            rs.set('hatenabookmark-%d' % page, 'False')
