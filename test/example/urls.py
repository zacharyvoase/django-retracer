# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
import django.http


urlpatterns = patterns('',
    url(r'^$', lambda req: django.http.HttpResponse(), name='index'),
    url(r'^feedback/$', 'feedback.views.feedback', name='feedback'),
)
