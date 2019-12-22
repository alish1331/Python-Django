
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.random_word),
    url(r'^random_word/$', views.random_word),
    url(r'^clear/$', views.clear),
]
