"""plus_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^seminar/', include('seminar.urls', namespace='seminar', app_name='seminar')),
    url(r'^problem/', include('problem.urls', namespace='problem', app_name='problem')),
    url(r'^shop/', include('shop.urls', namespace='shop', app_name='shop')),
    url(r'^', include('website.urls', namespace='website', app_name='website')),
    url(r'^seminar/', include('seminar.urls')),
    url(r'^problem/', include('problem.urls')),
    url(r'^', include('website.urls')),
]
