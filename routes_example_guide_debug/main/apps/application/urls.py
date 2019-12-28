from django.conf.urls import url
from . import views

print("in application urls.py")
print("trying this route: ")
print("localhost:8000")

# FIX

# print("localhost:8000/show")
# print("localhost:8000/dontshow")
# print("localhost:8000/showmorethings")

# FIX

# print("localhost:8000/show/15")

# FIX to actually show in html

# print("localhost:8000/show/13a23")

# FIX

# print('localhost:8000/editUser/15')
# print("localhost:8000/editUser/students_name")

urlpatterns = [
    url(r'^', views.index),
    
    url(r'show', views.showAll),
    
    url(r'^show/(?P<user_id>\d+)', views.showOne),
    
    url(r'^editUser/(?P<user_name>\w+)', views.editUser),

    url(r'^dontshow', views.dontshow),
    url(r'^showmorethings', views.showmorethings),
    



    
    
]

# localhost:8000
# localhost:8000/show
# localhost:8000/dontshow
# localhost:8000/showmorethings
# localhost:8000/show/15
# localhost:8000/show/15a23
# localhost:8000/editUser/15
# localhost:8000/editUser/students_name
