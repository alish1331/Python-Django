from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm_password):
        # Check for validation and then create the fields in table User
        validation_result = self.validate(
            first_name, last_name, email, password, confirm_password)
        # Result: result = {'status': True, 'errors': "Validation successful"}

        if validation_result['status'] == True:
            hashed_password = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt())
            created_user = self.create(
                first_name=first_name, last_name=last_name, email=email, password=hashed_password)

            validation_result = {
                'status': validation_result['status'],
                'created_user': created_user}

            return validation_result

        return validation_result

    def validate(self, first_name, last_name, email, password, confirm_password):
        errors = []
        result = {}
        #  Validate First Name
        if first_name == '':
            msg = "First name cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(first_name) < 2:
            msg = "First Name should have at least two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in first_name) == True:
            msg = "Name cannot have numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            #  Validate Last Name
        if last_name == '':
            msg = "Last name cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(last_name) < 2:
            msg = "First Name should have at least two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in last_name) == True:
            msg = "Name cannot have numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # Validate Email
        if email == '':
            msg = "Email cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif not emailRegex.match(email):
            msg = "Email is invalid"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(self.filter(email=email)) > 0:
            msg = "Email already exist in our database"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # Password Validation
        if password == '':
            msg = "Password cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(password) < 8:
            msg = "Password must be greater than 8 characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif not passwordRegex.match(password):
            msg = "Password must contain at least one lowercase letter, one uppercase letter, and one digit"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # Confirm Password
        elif confirm_password != password:
            msg = "Passwords do not match"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result

        else:
            result = {'status': True, 'errors': "Validation successful"}
            return result

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
            msg = "Please enter correct credentials"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result


class JobManager(models.Manager):
    # def validate_job(self, postData):
    def validate_job(self, job_title, desc, location, author):
        errors = []
        if job_title == '':
            msg = "Job title name cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(job_title) < 3:
            msg = "Job title should have at least 3 characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        if desc == '':
            msg = "Description cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(desc) < 2:
            msg = "Description should have at least 10 characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        if location == '':
            msg = "Location cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
         
        else:
            result = {'status': True, 'errors': "Successfully Created"}
            return result

    def edit_job_validate(self, job_title, desc, location):
        errors = []
        result = {}
        #  Validate First Name
        if job_title == '':
            msg = "Job title name cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(job_title) < 3:
            msg = "Job title should have at least 3 characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        if desc == '':
            msg = "Description cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(desc) < 2:
            msg = "Description should have at least 10 characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        if location == '':
            msg = "Location cannot be blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result

        else:
            result = {'status': True, 'errors': "Successfully Updated"}
            return result


    def add_favourite_for_user(self, user_id, job_id):
        job = Job.objects.get(id=job_id)
        current_user = User.objects.get(id=user_id)
        job.favouriting_users.add(current_user)
        result = {'status': True}
        return result

    def remove_from_favorites(self, user_id, job_id):
        job = Job.objects.get(id=job_id)
        current_user = User.objects.get(id=user_id)
        job.favouriting_users.remove(current_user)


class User(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=100, null=True)

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Job(models.Model):
    title = models.TextField(max_length=255, null=True)
    location = models.TextField(max_length=255, null=True)
    desc = models.TextField(max_length=2550, null=True)
    author = models.ForeignKey(User, related_name="jobs_posted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = JobManager()
