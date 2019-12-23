from django.shortcuts import render
from .models import User  #added this line to connect to db

# show all of the data from a table


def index(request):
    context = {
    	"all_users": User.objects.all()
    }
    return render(request, "users_app/index.html", context)
