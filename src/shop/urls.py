from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/buy$', views.ShopPurchaseView.as_view(), name='buy'),
    url(r'^(?P<pk>\d+)$', views.ShopListView.as_view(), name='list')
]
