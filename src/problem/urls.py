from django.conf.urls import url

from problem import views

urlpatterns = [
    url(r'^download/(?P<pk>\d+)$', views.DownloadView.as_view(), name='download'),
    url(r'^auth/(?P<pk>\d+)$', views.ProblemAuthView.as_view(), name='auth'),
    url(r'^get/(?P<pk>\d+)$', views.ProblemGetView.as_view(), name='get'),
    url(r'^$', views.ProblemListView.as_view(), name='list')
]
