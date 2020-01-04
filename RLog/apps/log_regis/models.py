from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

class RegManager(models.Manager):
    def register(self, request):
        if len(request.POST["name"]) < 2:
            messages.add_message(request, messages.ERROR, "Name is missing")
        if len(request.POST["last_name"]) < 2:
            messages.add_message(request, messages.ERROR, "Last name is missing")
        if len(request.POST["email"]) < 1:
            messages.add_message(request, messages.ERROR, "Email field can not be empty!")
        if not EMAIL_REGEX.match(request.POST["email"]):
            messages.add_message(request, messages.ERROR, "Invalid email address!")
        if len(request.POST["password"]) < 8:
            messages.add_message(request, messages.ERROR, "Password should be at least 8 characters!")
        if request.POST["password"] != request.POST["confirm"]:
            messages.add_message(request, messages.ERROR, "Password is not matching")
        if User.objects.filter(email=request.POST("email")).count() > 0:
            messages.add_message(request, messages.ERROR, "Email you used already exists. Please try other email.")

        if len(get_messages(request)) > 0:
            return False
        else:
            User.objects.create(
                name=request.POST["name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                password=bcrypt.hashpw(request.POST ["password"].encode(), bcrypt.gensalt())
            )
            return True

    def login(self, request):
            pass
        
class User(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = RegManager()
