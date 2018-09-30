"""knack_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include # Add include to the imports here
from django.contrib import admin

from . import views

urlpatterns = [
    url('^admin/', admin.site.urls),
    url(r'^$', views.DescriptionPageView.as_view(), name='description'),
    url(r'^description$', views.DescriptionPageView.as_view(), name='description'),
    url(r'^wysiwyg$', views.render_wysiwyg, name='wysiwyg'),
    url(r'^how_it_works$', views.render_how_it_works, name='how_it_works'),
    url(r'^contribute$', views.render_contribute, name='contribute'),
    url(r'^web_hosting$', views.WebHostingPageView.as_view(), name='web_hosting'),
    url(r'^getting_started/$', views.render_getting_started, name='getting_started'),
    url(r'^test$', views.render_test, name='test'),
    path('user/<str:username>/', views.render_user, name='user'),
    path('user/<str:username>/new_resource/', views.render_new_resource, name='new_resource'),
    path('user/<str:username>/new_blog/', views.render_new_blog, name='new_blog'),
    #path('user/<str:username>/<str:resourcename>/', views.render_resource, name='resource'),
    path('user/<str:username>/<str:blog_name>/', views.render_blog, name='blog'),
    path('user/<str:username>/<str:blog_name>/view/', views.render_view_blog, name='view_blog'),
    path('user/<str:username>/<str:blog_name>/edit/', views.render_edit_blog, name='edit_blog'),
    path('user/<str:username>/<str:blog_name>/fork/', views.render_fork_blog, name='fork_blog'),
    path('user/<str:username>/<str:blog_name>/new_post/', views.render_new_post, name='new_post'),
    path('user/<str:username>/<str:blog_name>/<str:post_name>/', views.render_post, name='post'),
    path('user/<str:username>/<str:blog_name>/<str:post_name>/view/', views.render_view_post, name='view_post'),
    path('user/<str:username>/<str:blog_name>/<str:post_name>/edit/', views.render_edit_post, name='edit_post'),
    path('user/<str:username>/<str:blog_name>/<str:post_name>/fork/', views.render_fork_post, name='fork_post'),
    #path('user/<str:username>/<str:resourcename>/edit/', views.render_edit_resource, name='edit_resource'),
    url(r'^', include('knack.urls'))
]
