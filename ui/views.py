from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from dictionaries import models
from ui import forms

SIGN_IN_USERNAME = 'sign_in_username'


def with_context(func):
    def __decorator(*args, **kwargs):
        context = {'view': args[0].resolver_match.view_name}
        return func(*args, **kwargs, context=context)

    return __decorator


@with_context
def index(request, context=None):
    # context.update({
    #     # 'header': '您关注的行业',
    #     # 'categories': models.Category.objects.filter(published=True),
    # })
    return render(request, 'index/index.html', context)


@with_context
def dictionaries(request, context=None):
    context.update({
        'dictionaries': models.Dictionary.objects.all()
    })
    return render(request, 'dictionaries/index.html', context)


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
