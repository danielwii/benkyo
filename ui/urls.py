# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'ui'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^dictionaries/$', views.dictionaries, name='dictionaries'),
    url(r'^dictionaries/(?P<dictionary_id>[0-9]+)/chapters/$',
        views.chapters, name='dictionaries-chapters'),

    url(r'^chapters/(?P<chapter_id>[0-9]+)/$',
        views.chapter_words, name='dictionaries-chapters-words'),
    url(r'^chapters/(?P<chapter_id>[0-9]+)/add-words$',
        views.chapter_add_words, name='dictionaries-chapters-add-words'),

    url(r'^learn/$', views.learn_index, name='learn'),
    url(r'^learn/(?P<selected_word_id>[0-9]+)/$', views.learn_word, name='learn-word'),
    url(r'^learn/(?P<selected_word_id>[0-9]+)/translation/$',
        views.learn_word_with_translation, name='learn-word-with-translation'),
    url(r'^learn/(?P<selected_word_id>[0-9]+)/next/$', views.learn_next, name='learn-next'),
    url(r'^learn/(?P<selected_word_id>[0-9]+)/ignore/$', views.learn_ignore, name='learn-ignore'),

    url(r'^sign-up/$', views.sign_up, name='sign-up'),
    url(r'^sign-in/$', views.sign_in, name='sign-in'),
    url(r'^sign-out/$', views.sign_out, name='sign-out'),
]
