# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dictionaries/$', views.dictionaries, name='dictionaries'),
    url(r'^sign-up/$', views.sign_up, name='sign-up'),
    url(r'^sign-in/$', views.sign_in, name='sign-in'),
    url(r'^sign-out/$', views.sign_out, name='sign-out'),
]
