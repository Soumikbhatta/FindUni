"""finduni URL Configuration

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
from django.contrib import admin
from django.urls import path
from api import views
from finduni import views as mviews

urlpatterns = [
    path('', mviews.index),
    path('collegeprob/', mviews.colprob),
    path('predictcol/', mviews.predcol),
    path('convertgpa/', mviews.convertgpa),
    path('contact/', mviews.contact),
    path('admin/', admin.site.urls),
    path('college-prob/', views.collegeProbability),
    path('college-apply-list/', views.collegeApplyList),
    path('india-exam/', views.ind_exam),
    path('india-test/', mviews.ind_test),
    path('india-coll/', mviews.ind_college),
    path('india-colle/', views.ind_coll),
    path('send-mail/', views.contact_us)
]
