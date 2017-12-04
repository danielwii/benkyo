from django.shortcuts import render

from dictionaries import models


def with_context(func):
    def __decorator(*args, **kwargs):
        context = {0: 1}
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
