from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

# Returns error message if any of required filers is missing or wrong
class UserManager(models.Manager):
    def register(self, request):
        if len(request.POST["name"]) < 2:
            messages.add_message(request, messages.ERROR, "Name is required!")
        if len(request.POST["last_name"]) < 2:
            messages.add_message(request, messages.ERROR, "Last name is required!")
        if len(request.POST["email"]) < 2:
            messages.add_message(request, messages.ERROR, "Email is required!")
        if not EMAIL_REGEX.match(request.POST["email"]):
            messages.add_message(request, messages.ERROR, "Invalid email format! Ex: codingdojo@test.com")
        if len(request.POST["password"]) < 8:
            messages.add_message(request, messages.ERROR, "Password must be between 8-32 characters!")
        if request.POST["password"] != request.POST["confirm"]:
            messages.add_message(request, messages.ERROR, "Password and Password Confirmation must match!")
        if User.objects.filter(email=request.POST["email"]).count() > 0:
            messages.add_message(request, messages.ERROR, "A user with this email already exists!")

        if len(get_messages(request)) > 0:
            return False

# uploads info into the User table
        else:
            User.objects.create(
                name=request.POST["name"],
                last_name = request.POST["last_name"],
                email=request.POST["email"],
                password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            )
            return True

    def login(self, request):
        pass

# Models
class User(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

# class Message(models.Model):
#     message = models.TextField(max_length=1024)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     user = models.ForeignKey(User, related_name="user_comments")


# class Comment(models.Model):
#     comment = models.TextField(max_length=1024)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     user = models.ForeignKey(User, related_name="user_comments")
#     message = models.ForeignKey(User, related_name="user_messages")

class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")


class Review(models.Model):
    text = models.CharField(max_length=255)
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="user_reviews")
    book = models.ForeignKey(Book, related_name="book_reviews")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

