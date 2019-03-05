"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^myapp/',include('myapp.urls')),
    url(r'^about/$',views.about),
    url(r'^$',views.homepage),
    url(r'^login/', views.login),
    url(r'^analysis/',views.analysis),
    url(r'^index/', views.index),
    url(r'^smallschool/', views.home),
    url(r'^home/', views.home),
    url(r'^stock_ana/', views.stock_analysis),
    url(r'^signin/', views.register),
    url(r'^forgot/', views.getpassword),

    url(r'^get_news/', views.get_news),
    url(r'^search/', views.search_news),
    url(r'^search/', views.search_news),
    


]

urlpatterns += staticfiles_urlpatterns()
#herry future123
