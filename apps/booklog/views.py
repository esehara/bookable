# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.booklog.models import BookLog


def latest(request):
    return render(
        request,
        'latest.html',
        BookLog.return_page_click_dict())
