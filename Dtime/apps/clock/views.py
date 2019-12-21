from django.shortcuts import render
from time import gmtime, strftime


def index(request):
    context = {
        "date": strftime("%b %d", gmtime()),
        "time": strftime("%Y %I:%M%p", gmtime())
    }
    return render(request, 'clock_t/index.html', context)
