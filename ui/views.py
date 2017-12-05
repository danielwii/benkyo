from random import randint

import django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from core.mem_curve import Ranks
from dictionaries import models
from ui import forms

SIGN_IN_USERNAME = 'sign_in_username'


def with_context(func):
    def __decorator(*args, **kwargs):
        context = {'view_name': args[0].resolver_match.view_name}
        return func(*args, **kwargs, context=context)

    return __decorator


@with_context
def index(request, context=None):
    # context.update({
    #     # 'header': '',
    #     # 'categories': models.Category.objects.filter(published=True),
    # })
    return render(request, 'index/index.html', context)


@with_context
def dictionaries(request, context=None):
    dictionaries_with_counts = models.Dictionary.objects.annotate(Count('chapters__words'))
    context.update({
        'dictionaries_with_counts': dictionaries_with_counts
    })
    return render(request, 'dictionaries/index.html', context)


@with_context
def chapters(request, dictionary_id, context=None):
    chapters_words = models.Chapter.objects \
        .filter(dictionary_id=dictionary_id) \
        .annotate(Count('words'))
    selected_words = models.SelectedWord.objects \
        .filter(owner=request.user.profile) \
        .values('origin__chapter').order_by() \
        .annotate(Count('origin'))

    chapters_with_words = []
    for chapter in chapters_words:
        selected = list(filter(lambda s: s['origin__chapter'] == chapter.id, selected_words))
        if len(selected) == 1:
            chapters_with_words.append((chapter, selected[0]))
        else:
            chapters_with_words.append((chapter, {'origin__chapter': chapter.id, 'origin__count': 0}))
    context.update({
        'chapters_with_words': chapters_with_words,
    })
    return render(request, 'dictionaries/chapters.html', context)


@with_context
def chapter_words(request, chapter_id, context=None):
    chapter = models.Chapter.objects.get(pk=chapter_id)
    context.update({
        'chapter': chapter
    })
    return render(request, 'dictionaries/chapter.html', context)


@with_context
def sign_up(request, context=None):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.clean_password2()
            user = User.objects.create_user(username, None, password)
            context.update({'current_user': user})
            request.session[SIGN_IN_USERNAME] = username
            return render(request, 'user/success.html', context)
    else:
        user_form = UserCreationForm()

    context.update({'user_form': user_form})
    return render(request, 'user/sign_up.html', context)


@with_context
def sign_in(request, context=None):
    if request.POST:
        login_form = forms.UserLoginForm(request.POST)
        username = login_form.data['username']
        password = login_form.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context.update({'errors': '用户名或密码错误，无法登录。'})
    else:
        username = None
        if SIGN_IN_USERNAME in request.session:
            username = request.session[SIGN_IN_USERNAME]
        login_form = forms.UserLoginForm(initial={'username': username})

    context.update({'login_form': login_form})
    return render(request, 'user/sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('/')


def chapter_add_words(request, chapter_id):
    """
    add all chapter words to current user's selected words
    :param request:
    :param chapter_id:
    :return:
    """
    user = request.user
    chapter = get_object_or_404(models.Chapter, pk=chapter_id)
    for word in chapter.words.all():
        try:
            user.profile.selected_words.create(origin=word)
        except django.db.utils.IntegrityError:
            pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@with_context
def learn_index(request, context=None):
    # 1. ranks < 10
    ranks_lt_10_count = models.SelectedWord.objects \
        .filter(owner=request.user.profile) \
        .filter(ranks__lt=Ranks.NOT_REMEMBER_TOTALLY) \
        .count()
    current = models.SelectedWord.objects \
        .filter(owner=request.user.profile) \
        .filter(ranks__lt=Ranks.NOT_REMEMBER_TOTALLY) \
        .all()[randint(0, ranks_lt_10_count - 1)]
    context.update({
        'ranks_lt_10_count': ranks_lt_10_count,
        'current': current,
    })
    return render(request, 'learn/index.html', context)


@with_context
def learn_word(request, word_id, context=None):
    return None
