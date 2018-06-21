from django.conf.urls import url

from problem import views

app_name = 'problem'

urlpatterns = [
    url(r'^download/(?P<pk>\d+)$', views.ProblemDownloadView.as_view(), name='download'),
    url(r'^auth/(?P<pk>\d+)$', views.ProblemAuthView.as_view(), name='auth'),
    url(r'^get/(?P<pk>\d+)$', views.ProblemGetView.as_view(), name='get'),
    url(r'^rank/(?P<pk>\d+)$', views.ProblemRankView.as_view(), name='rank'),
    url(r'^rank/$', views.ProblemRankView.as_view(), name='rank'),
    url(r'^question/$', views.ProblemQuestionView.as_view(), name='question'),
    url(r'^$', views.ProblemListView.as_view(), name='list')
]
