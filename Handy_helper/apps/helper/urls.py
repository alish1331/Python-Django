from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),

    # url(r'^jobs$', views.jobs),

    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^new$', views.new),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^details/(?P<id>\d+)$', views.details),
    url(r'^delete/(?P<id>\d+)$', views.delete),

    # url(r'^job/(?P<job_id>\d+)$', views.add_favorite_for_current_user),
    # url(r'^remove/(?P<job_id>\d+)$', views.remove_from_favourites),
]
