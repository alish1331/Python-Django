from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User, RegManager
from django.contrib import messages

import bcrypt


def index(request):
    return render(request, "log_regis/index.html")

def register(request):
    if request.method == "POST":
        # print("*"*60)
        User.objects.register(request)
        return redirect("log_regis/success.html")
    else:
        # messages.add_message(request, messages.ERROR, "Please fill in all the fields to register.")
        return redirect("/")

def login(request):
    try:
        user = User.objects.get(email=request.POST["email"])
        valid = bcrypt.checkpw(request.POST["password"].encode(), user.password.encode())

        if valid:
            print("**** Password is correct *****")
            return redirect("/success")
        else:
            print("**** Password does NOT match ****")
            message.add_message(request, message.ERROR, "Invalid password!")
            return redirect("/")
    except:
        messages.add_message(request, messages.ERROR, "No user with this email was found! Please register.")
        return redirect("/")
        
def success(request):
    return redirect("log_regis/success.html")
