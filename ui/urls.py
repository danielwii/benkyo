# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^dictionaries/$', views.dictionaries, name='dictionaries'),
    url(r'^dictionaries/(?P<dictionary_id>[0-9]+)/chapters/$', views.chapters, name='dictionaries-chapters'),
    url(r'^chapters/(?P<chapter_id>[0-9]+)/$', views.chapter_words, name='dictionaries-chapters-words'),

    url(r'^chapters/(?P<chapter_id>[0-9]+)/add-words$', views.chapter_add_words, name='dictionaries-chapters-add-words'),

    url(r'^learn/$', views.learn_index, name='learn'),
    url(r'^learn/(?P<word_id>[0-9]+)/$', views.learn_word, name='learn-word'),

    url(r'^sign-up/$', views.sign_up, name='sign-up'),
    url(r'^sign-in/$', views.sign_in, name='sign-in'),
    url(r'^sign-out/$', views.sign_out, name='sign-out'),
]
