from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

def index(request):
    return render(request, 'randomW_t/index.html')


def random_word(request):
    new_word = get_random_string(length=14)

    if 'counter' not in request.session:
            request.session['counter'] = 0
    else:
        request.session['counter'] += 1
    context = {
        'counter': request.session['counter'],
        'new_word': new_word
    }

    return render(request, 'randomW_t/index.html', context)

def clear(request):
    try:
        request.session['counter'] = 0
    except KeyError:
        pass
    context = {
        'counter': request.session['counter'],
    }
    return render(request, 'randomW_t/index.html', context)
