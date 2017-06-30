from django.conf.urls import url
from django.contrib.auth import views as auth_views

from website import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^seminar/$', views.SeminarListView.as_view(), name='seminar'),
    url(r'^download/$', views.DownloadView.as_view(), name='download')
]
