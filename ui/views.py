from random import randint

import django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from logzero import logger

from core.mem_curve import Ranks
from dictionaries import models, services
from ui import forms

SIGN_IN_USERNAME = 'sign_in_username'
LEFT_WORDS = 'left_words'


def with_logged_context(func):
    @login_required(login_url='/sign-in')
    def __decorator(*args, **kwargs):
        context = {
            'view_name': args[0].resolver_match.view_name,
            'left_words': left_words(args[0]).count() if left_words(args[0]) else 0,
        }
        return func(*args, **kwargs, context=context)

    return __decorator


LEFT_FILTER = Q(ranks__lt=Ranks.NOT_REMEMBER_TOTALLY) | \
              Q(next_check_point__isnull=True) | \
              Q(next_check_point__lte=timezone.now())


def left_words(request):
    if request.user.is_authenticated:
        return models.SelectedWord.objects.filter(owner=request.user.profile).filter(LEFT_FILTER)


@with_logged_context
def index(request, context=None):
    return render(request, 'index/index.html', context)


@with_logged_context
def dictionaries(request, context=None):
    dictionaries_words = models.Dictionary.objects \
        .annotate(count=Count('chapters__words'))
    selected_words = models.SelectedWord.objects \
        .filter(owner=request.user.profile) \
        .values('origin__chapter__dictionary').order_by() \
        .annotate(count=Count('origin'))

    dictionaries_with_words = []
    for dictionary in dictionaries_words:
        selected = list(filter(lambda s: s['origin__chapter__dictionary'] == dictionary.id, selected_words))
        if len(selected):
            dictionaries_with_words.append((dictionary, selected[0]))
        else:
            dictionaries_with_words.append((dictionary, {'origin__chapter__dictionary': dictionary.id, 'count': 0}))

    context.update({
        'dictionaries_with_words': dictionaries_with_words
    })
    return render(request, 'dictionaries/index.html', context)


@with_logged_context
def chapters(request, dictionary_id, context=None):
    chapters_words = models.Chapter.objects \
        .filter(dictionary_id=dictionary_id) \
        .annotate(count=Count('words'))
    selected_words = models.SelectedWord.objects \
        .filter(owner=request.user.profile) \
        .values('origin__chapter').order_by() \
        .annotate(count=Count('origin'))

    chapters_with_words = []
    for chapter in chapters_words:
        selected = list(filter(lambda s: s['origin__chapter'] == chapter.id, selected_words))
        if len(selected) == 1:
            chapters_with_words.append((chapter, selected[0]))
        else:
            chapters_with_words.append((chapter, {'origin__chapter': chapter.id, 'count': 0}))

    context.update({
        'chapters_with_words': chapters_with_words,
    })
    return render(request, 'dictionaries/chapters.html', context)


@with_logged_context
def chapter_words(request, chapter_id, context=None):
    chapter = models.Chapter.objects.get(pk=chapter_id)
    context.update({
        'chapter': chapter
    })
    return render(request, 'dictionaries/chapter.html', context)


def sign_up(request):
    context = {}
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


def sign_in(request):
    context = {}
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


@with_logged_context
def chapter_add_words(request, chapter_id, context=None):
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
        except django.db.utils.IntegrityError as e:
            logger.exception(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@with_logged_context
def learn_index(request, context=None):
    current = left_words(request).all()[randint(0, context[LEFT_WORDS] - 1)]
    context.update({
        'current': current,
    })
    return render(request, 'learn/index.html', context)


@with_logged_context
def learn_word_with_translation(request, selected_word_id, context=None):
    current = models.SelectedWord.objects.get(owner=request.user.profile, origin=selected_word_id)
    context.update({
        'current': current,
        'with_translation': True
    })
    return render(request, 'learn/with-translation.html', context)


@with_logged_context
def learn_word(request, selected_word_id, context=None):
    current = models.SelectedWord.objects.get(owner=request.user.profile, origin=selected_word_id)
    if request.POST:
        choice = request.POST['choice']
        services.learn_word(current, int(choice))
    if request.POST['with-translation'] == str(True):
        return redirect('ui:learn')
    else:
        return redirect('ui:learn-next', selected_word_id=selected_word_id)


@with_logged_context
def learn_next(request, selected_word_id, context=None):
    current = models.SelectedWord.objects.get(owner=request.user.profile, origin=selected_word_id)
    context.update({
        'current': current,
    })
    return render(request, 'learn/next.html', context)
