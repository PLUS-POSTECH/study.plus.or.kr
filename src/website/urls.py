from django.conf.urls import url
from django.contrib.auth import views as auth_views

from website import views

app_name = "website"

urlpatterns = [
    url(r"^$", views.HomeView.as_view(), name="home"),
    url(r"^login/$", auth_views.LoginView.as_view(), name="login"),
    url(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"^register/$", views.RegisterView.as_view(), name="register"),
]
