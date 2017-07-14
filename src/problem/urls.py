from django.conf.urls import url

from problem import views

urlpatterns = [
    url(r'^download$', views.DownloadView.as_view(), name='download_problem'),
    url(r'^auth$', views.ProblemAuthForm.as_view(), name='auth_problem'),
    url(r'^get$', views.ProblemGetForm.as_view(), name='get_problem'),
    url(r'^', views.ProblemListView.as_view(), name='list_problem')
]
