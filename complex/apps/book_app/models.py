from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def register(self, request):
        if len(request.POST["name"]) < 2:
            messages.add_message(request, messages.ERROR, "Name is required!")
        if len(request.POST["last_name"]) < 2:
            messages.add_message(request, messages.ERROR, "Last name is required!")
        if len(request.POST["email"]) < 1:
            messages.add_message(request, messages.ERROR, "Email is required!")
        if not EMAIL_REGEX.match(request.POST["email"]):
            messages.add_message(request, messages.ERROR,
                                    "Invalid email format! Ex: testemail@testemail.com")
        if len(request.POST["password"]) < 8:
            messages.add_message(request, messages.ERROR,
                                    "Password must be between 8-32 characters!")
        if request.POST["password"] != request.POST["confirm"]:
            messages.add_message(request, messages.ERROR,
                                    "Password and Password Confirmation must match!")
        if User.objects.filter(email=request.POST["email"]).count() > 0:
            messages.add_message(request, messages.ERROR,
                                    "A user with this email already exists!")

        if len(get_messages(request)) > 0:
            return False
        else:
            User.objects.create(
                name=request.POST["name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            )
            return True

    def login(self, request):
        pass


class User(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user


class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    uploded_by = models.ForeignKey(
        User, related_name="books_uploaded", default=None)
    # uploaded_by = user who uploaded a given book
    users_who_like = models.ManyToManyField(
        User, related_name="liked_books", default=None)
    # users_who_like = a list of users who like a given book

class Review(models.Model):
    text = models.CharField(max_length=255)
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="user_reviews")
    book = models.ForeignKey(Book, related_name="book_reviews")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
