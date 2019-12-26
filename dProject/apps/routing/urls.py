from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new/$', views.new),
    url(r'^create/$', views.index),
    url(r'^[0-9]{2}/$', views.show),
]
