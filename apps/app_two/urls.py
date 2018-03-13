from django.conf.urls import url, include
from . import views

# This is app_one
urlpatterns = [
# root route to index method
    url(r'^$', views.index, name='index'),
    url(r'^all_users/$', views.all_users, name='all_users'),
    url(r'^connect/(?P<user_id>\d+)$', views.connect, name='connect'),
    url(r'^users/(?P<user_id>\d+)$', views.users, name='users'),
    url(r'^accept/(?P<id>\d+)$', views.accept, name='accept'),
    url(r'^ignore/(?P<id>\d+)$', views.ignore, name='ignore'),
]
