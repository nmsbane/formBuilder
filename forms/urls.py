from django.conf.urls import include, url
from django.views.generic import TemplateView

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
    url(r'^shareform/(?P<form_id>[0-9]+)/$', views.share_form, name='share_form'),
    url(r'^thanks/$',TemplateView.as_view(template_name='forms/thanks.html') ),
    
]

