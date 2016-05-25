from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login')    
    #(r'^accounts/login/$', custom_login),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.custom_login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^newform/$', views.newform, name='add_form'),
    url(r'^createform/$', views.create_form, name='create_form'),
    
]

