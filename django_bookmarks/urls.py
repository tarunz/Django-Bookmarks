"""django_bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to ur
    url(r'^login/$','django.contrib.auth.views.login'),lpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os.path
from django.conf.urls import include, url
from django.contrib import admin
# from django.conf.urls.defaults import *
from bookmarks.views import *
from django.views.generic import TemplateView
site_media=os.path.join(os.path.dirname(__file__),'site_media')
# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
# ]
urlpatterns = [
	# (r'^django_bookmarks/',include('django_bookmarks.foo.urls')),
	url(r'^admin/', include(admin.site.urls)),
	# (r'^admin/', include('django.contrib.admin.urls')),
	# Browsing 
	url(r'^$',main_page),
	url(r'^user/(\w+)/$',user_page),
	# Session Management 
	url(r'^login/$','django.contrib.auth.views.login'),
	url(r'^logout/$',logout_page),
	url(r'^site_media/(?P<path>.*)$',
		'django.views.static.serve',
		{'document_root':site_media}),
	url(r'^register/$',register_page),
	url(r'^register/success/$',TemplateView.as_view(
		template_name="registration/register_success.html"
		)),
	#Account Management
	url(r'^save/$',bookmark_save_page),
	url(r'^tag/([^\s]+)/$',tag_page),
	url(r'^tag/$',tag_cloud_page),
	]
	# +static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
