"""CardioCardOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cconline.views.index',  name='index'),#index page
    url(r'^patients/my/', 'cconline.views.get_my_patient', name='my_patient'),
    url(r'^patient/(?P<idpatient>\d+)/$', 'cconline.views.get_patient', name='get_patient'),
    url(r'^diary/list/(?P<idpatient>\d+)/$', 'cconline.views.get_diary_list', name='list_diary'),
    url(r'^diary/(?P<id>\d+)/$', 'cconline.views.get_diary', name='get_diary'),
#    url(r'^examens/list/(?P<idpatient>\d+)/$', 'cconline.views.get_my_patient', name='my_patient'),
    url(r'^laboratory/list/(?P<idpatient>\d+)/$', 'cconline.views.get_lab_list', name='list_lab'),
    url(r'^labs/(?P<id>\d+)/$', 'cconline.views.get_laboratory', name='get_lab'),
#    url(r'^medication/list/(?P<idpatient>\d+)/$', 'cconline.views.get_my_patient', name='my_patient'),
#    url(r'^proffview/list/(?P<idpatient>\d+)/$', 'cconline.views.get_my_patient', name='my_patient'),
#    url(r'^nurse/list/(?P<idpatient>\d+)/$', 'cconline.views.get_my_patient', name='my_patient'),
]
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()