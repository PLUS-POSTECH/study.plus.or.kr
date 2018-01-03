from django.conf.urls import url

from seminar import views

urlpatterns = [
    url(r'^download/(?P<pk>\d+)$', views.SeminarDownloadView.as_view(), name='download'),
    url(r'^edit(?:/(?P<pk>\d+))?$', views.SeminarEditView.as_view(), name='edit'),
    url(r'^$', views.SeminarListView.as_view(), name='list')
]
