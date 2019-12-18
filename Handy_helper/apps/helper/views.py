from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib import messages
from django.contrib.auth import authenticate
import re
from .models import User, Job

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


def index(request):
    request.session.clear()
    return render(request, 'helper/index.html')


def login_validate(self, email, password):
        errors = []
        try:
            found_user = self.get(email=email)
            if bcrypt.checkpw(password.encode(), found_user.password.encode()):
                result = {'status': True, 'found_user': found_user}
                return result
            else:
                msg = "Email and Password do not match"
                errors.append(msg)
                result = {'status': False, 'errors': errors[0]}
                return result
        except:
            msg = "Email is not in our database"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result


def register(request):
    if request.method == "GET":
        return redirect('/')

    new_user = User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                                     request.POST['password'], request.POST['confirm_password'])

    if new_user['status'] == True:
        request.session['id'] = new_user['created_user'].id
        return redirect('/dashboard')
    else:
        messages.error(request, new_user['errors'], extra_tags="register")
        return redirect('/')


def login(request):
    if request.method == "GET":
        return redirect('/')

    current_user = User.objects.login_validate(
        request.POST['email'], request.POST['password'])

    if current_user['status'] == True:
        request.session['id'] = current_user['found_user'].id
        return redirect('/dashboard')
    else:
        messages.error(request, current_user['errors'], extra_tags="login")
        return redirect('/')


def dashboard(request):
    current_user = User.objects.get(id=request.session['id'])
    alljobs = Job.objects.all().order_by('-id')

    context = {
        "current_user": current_user,
        "prods": alljobs,
    }
    return render(request, "helper/dashboard.html", context)




def new(request):
    if request.method == "GET":
    
        current_user = User.objects.get(id=request.session['id'])
        context = {
            "current_user": current_user,
        }

        return render(request, "helper/new_job.html", context)

    if request.method == "POST":

        title = request.POST['job_title']
        desc = request.POST['desc']
        location = request.POST['location']
        author = User.objects.get(id=request.session['id'])

        # Validate secret before creating, pass arguments to validate function
        result = Job.objects.validate_job(title, desc, location, author)
        if result['status'] == True:
           
            result = Job.objects.create(
                title=title, location=location, desc=desc, author=author)
            return redirect('/dashboard')

        else:
            messages.error(request, result['errors'], extra_tags="job_post")
            return redirect('/new')

        
    return redirect('/dashboard')




def edit(request, id):
    if request.method == "GET":

        job = Job.objects.get(id=id)

        context = {
            'job':job
        }

        return render(request, 'helper/edit.html', context)

    if request.method == "POST":
        j = Job.objects.get(id=id)
        result = Job.objects.edit_job_validate(
            request.POST['job_title'], request.POST['desc'], request.POST['location'])
        if result['status'] == True:
            j.job_title = request.POST['job_title']
            j.desc = request.POST['desc']
            j.location = request.POST['location']
            j.save()
            messages.info(request, result['errors'])
        else:
            messages.error(request, result['errors'])
            # return redirect('/dashboard')
            return redirect('/edit/' + str(j.id))

    return redirect('/dashboard')


def details(request, id):
    details = Job.objects.get(id=id)
    user_id = request.session['id']
    context = {
        "job": details,
        "user": user_id
    }

    return render(request, 'helper/details.html', context)


def delete(request, id):

    job = Job.objects.get(id=id)
    job.delete()

    return redirect('/dashboard')