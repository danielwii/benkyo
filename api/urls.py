# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^dictionaries/$', views.DictionaryListView.as_view(), name='dictionary-list'),
    url(r'^dictionaries/(?P<pk>[0-9]+)/$', views.DictionaryDetailView.as_view(), name='dictionary-detail'),
    url(r'^chapters/(?P<pk>[0-9]+)/$', views.ChapterDetailView.as_view(), name='chapter-detail'),
]
