from django.shortcuts import render, HttpResponse, redirect
from django.conf.urls import url
from . import views

def index(request):
    return HttpResponse('<h1 style="color:red">Main: Placeholder to later display a list of all blogs</h1> <p>add /new in the URL to continue</p>')

def new(request):
    return HttpResponse('<h1 style="color:red">New: Placeholder to later display a list of all blogs</h1><p>in the URL replace /new with /create to ger redirected back to main</p>')
# Create your views here.

def create(request):
    return redirect("/")

def show(number):
    number_from_form = int(request.form['number'])
    return render('./templates/show.html', number_from_form=int(number))
