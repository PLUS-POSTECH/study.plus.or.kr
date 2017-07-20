from django.conf.urls import url

from seminar import views

urlpatterns = [
    url(r'^download$', views.DownloadView.as_view(), name='download_seminar'),
    url(r'^', views.SeminarListView.as_view(), name='seminar')
]
