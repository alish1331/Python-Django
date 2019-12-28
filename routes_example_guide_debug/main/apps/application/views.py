from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request,'application/index.html')

def showAll(request):
    return render(request, 'application/all.html')
    
def dontshow(request):
    return redirect('/')


def showmorethings(request, sometext):
    context = {
        "id": sometext
    }
    return render(request, 'application/one.html', context)

def showOne(request, user_id):
    
    # doesn't use the user_id...
    context = {
        "id": user_id
    }
    return render(request,'application/one.html', context)

def editUser(request, user_name):

    # nothing here ?
    print(user_name, '*'*50)

    return render(request, 'application/edit.html', {"name": user_name})

# localhost:8000
# localhost:8000/show
# localhost:8000/dontshow
# localhost:8000/showmorethings
# localhost:8000/show/15
# localhost:8000/show/15a23
# localhost:8000/edit/students_name
