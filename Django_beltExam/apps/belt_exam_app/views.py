from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib import messages
# from django.contrib.auth.forms import NameChangeForm
import re
from .models import User, Quote

# Create your views here.


def index(request):
    return render(request, "belt_exam_app/index.html")


def users(request, user_id):
    author = User.objects.get(id=user_id)
    context = {
        'quotes': Quote.objects.filter(author=author),
        'author': author
    }
    return render(request, "belt_exam_app/users.html", context)


def myaccount(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    return render(request, "belt_exam_app/myaccount.html", context)


def quotes(request):
    registered_users = User.objects.all()
    current_user = User.objects.get(id=request.session['id'])
    favourites = Quote.objects.filter(favouriting_users=current_user)
    allquotes = Quote.objects.all().order_by(
        '-id').exclude(id__in=[f.id for f in favourites])

    context = {
        "registered_users": registered_users,
        "current_user": current_user,
        "quotes": allquotes,
        "favourites": favourites
    }

    return render(request, "belt_exam_app/quotes.html", context)


def register(request):
    # if get request; redirect to index
    if request.method == "GET":
        return redirect('/')
    # if validation successful (User.objects.register should return True),
    # store id in req.session
    new_user = User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                                     request.POST['password'], request.POST['confirm_password'])
    if new_user['status'] == True:
        request.session['id'] = new_user['created_user'].id
        return redirect('/quotes')
    else:
        messages.error(request, new_user['errors'], extra_tags="register")
        return redirect('/')


def login(request):
    # if get request; redirect to index
    if request.method == "GET":
        return redirect('/')
    current_user = User.objects.login_validate(
        request.POST['email'], request.POST['password'])
    if current_user['status'] == True:
        request.session['id'] = current_user['found_user'].id
        return redirect('/quotes')
    else:
        messages.error(request, current_user['errors'], extra_tags="login")
        return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')


def quote_post(request):
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        quote_text = request.POST['quote']
        user_id = request.session['id']
        quoted_by = request.POST['quote_author']
#
        # Validate secret before creating, pass arguments to validate function
        result = Quote.objects.validate_quote(quote_text, user_id, quoted_by)
        if result['status'] == True:
            messages.info(request, result['errors'])
            return redirect('/quotes')
        messages.error(request, result['errors'], extra_tags="quote_post")
        return redirect('/quotes')


def add_favorite_for_current_user(request, quote_id):
    user_id = request.session['id']
    Quote.objects.add_favourite_for_user(user_id, quote_id)
    return redirect('/quotes')


def remove_from_favourites(request, quote_id):
    user_id = request.session['id']
    Quote.objects.remove_from_favorites(user_id, quote_id)
    return redirect('/quotes')


def dashboard(request):
    return redirect('/quotes')

def edit_user(request, user_id):
    # print('--->',request.session['id'])
    user = User.objects.get(id=request.session['id'])
    
    context= {
        'user':user
    }
    # print('{user.id}')
    return render(request, 'belt_exam_app/myaccount.html', context)


def update_user(request, user_id):
    
    if request.method == "POST":
        u = User.objects.get(id=user_id)
        result = User.objects.edit_account_validate(
            request.POST['first_name'], request.POST['last_name'], request.POST['email'])
        if result['status'] == True:
            u.first_name = request.POST['first_name']
            u.last_name = request.POST['last_name']
            u.email = request.POST['email']
            u.save()
            messages.info(request, result['errors'])
        else:
            messages.error(request, result['errors'])
            return redirect('/myaccount/' + str(u.id))

    # if request.method == "POST":
    #     l = User.objects.get(id=user_id)
    #     l.last_name = request.POST['last_name']
    #     l.save()

    return redirect('/myaccount/' + str(u.id))
    # return redirect(f'/myaccount/{user_id}')
