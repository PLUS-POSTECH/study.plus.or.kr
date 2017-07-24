from django.conf.urls import url

from seminar import views

urlpatterns = [
    url(r'^download/(?P<pk>\d+)$', views.DownloadView.as_view(), name='download'),
    url(r'^$', views.SeminarListView.as_view(), name='list')
]
