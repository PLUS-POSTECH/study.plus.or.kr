from django.conf.urls import url

from problem import views

urlpatterns = [
    url(r'^download/$', views.DownloadView.as_view(), name='download'),
    url(r'^', views.ProblemListView.as_view(), name='problem')
]
