# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.booklog.models import BookLog


def latest(request):
    page = request.GET.get('page', 1)
    d = BookLog.return_page_click_dict(page=int(page) - 1)
    d['return_url'] = "latest?page=%d" % (int(page) + 1)
    return render(
        request,
        'latest.html',
        d)
