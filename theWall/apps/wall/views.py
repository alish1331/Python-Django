from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import User, Author, Book, Review
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, "wall/index.html")


def register(request):
    if request.method == "POST":
        User.objects.register(request)
        messages.add_message(request, messages.SUCCESS, "Congrats! You succesfully signed up.")
        return redirect("/")
        
    else:
        return redirect("/")


def login(request):
    try:
        user = User.objects.get(email=request.POST["email"])

        print("User name: " + user.name)
        request.session["name"] = user.name
        #request.session["name"] = User.objects.get("name")
        # print("*"*50)
        print("Session User Name: " + request.session["name"])
        
        isValid = bcrypt.checkpw(
            request.POST["password"].encode(), user.password.encode())

        print("is valid pwd? - " + isValid)

        if isValid:
            print("PASSWORDS MATCH")
            #print("user id: " + user.id)
            #request.session["user.id"] = user.id
            print("*"*50)
            print("Session User Name: " + request.session["name"])
            return redirect("/books", name=request.session["name"])
        else:
            print("NO MATCH")
            messages.add_message(request, messages.ERROR, "Invalid Credentials!")
            return redirect("/")
    except:
        messages.add_message(request, messages.ERROR, "No user with this email was found!")
        return redirect("/")


def books(request, name):
    print("*"*50)
    print("Inside /books")
    latestReviews = Review.objects.all().order_by("-id")[:3]
    otherReviews = Review.objects.all().order_by("-id")[3:]

    b_name = Book.objects.all()
    books = {
        "name": b_name
    }
    print("*"*50)
    print("Books Session User Name: " + request.session["name"])
    context = {
        "reviews": latestReviews,
        "otherReviews": otherReviews
        #"name": User.objects.get(id=request.session["user.id"])
    }

    return render(request, "wall/b.html", context, books)


def addBook(request):
    authors = Author.objects.all()
    return render(request, "wall/addBook.html", {
        "authors": authors
    })


def createBook(request):
    if len(request.POST["author"]) < 1 and len(request.POST["newAuthor"]) < 1:
        messages.add_message(request, messages.ERROR,
                             "You need to supply an author name!")
        return redirect("/books")

    if request.POST["author"]:
        author = int(request.POST["author"])

    newAuthor = ""

    if len(request.POST["newAuthor"]) > 0:
        newAuthor = Author.objects.create(
            name=request.POST["newAuthor"]
        )
        author = newAuthor.id

    book = Book.objects.create(
        title=request.POST["title"],
        author_id=author
    )

    review = Review.objects.create(
        text=request.POST["review"],
        rating=request.POST["rating"],
        user_id=1,
        book_id=book.id
    )

    return redirect("/books")


def showBook(request, id):
    book = Book.objects.get(id=id)
    reviews = Review.objects.filter(book_id=id)

    context = {
        "book": book,
        "reviews": reviews
    }
    return render(request, "wall/showBook.html", context)
