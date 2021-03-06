from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quote$', views.quote_post),
    url(r'^dashboard$', views.dashboard),
    url(r'^quote/(?P<quote_id>\d+)$', views.add_favorite_for_current_user),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove_from_favourites),
    url(r'^users/(?P<user_id>\d+)$', views.users),
    url(r'^myaccount/(?P<user_id>\d+)$', views.edit_user),
    url(r'^edit_user/(?P<user_id>\d+)$', views.update_user),
    # url(r'^update_user/(?P<user_id>\d+)$', views.update_user),
]
