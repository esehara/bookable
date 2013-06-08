# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.shelf import models

admin.site.register(models.Book)
admin.site.register(models.Keyword)
admin.site.register(models.KeywordToBook)
