from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^manager/', include(admin.site.urls)),
    url(r'', include('apps.shelf.urls')),
)
