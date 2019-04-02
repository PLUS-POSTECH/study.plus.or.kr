from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^prod/(?P<pk>\d+)/buy$', views.ShopPurchaseView.as_view(), name='buy'),
    url(r'^prod/(?P<pk>\d+)$', views.ShopProdView.as_view(), name='prod'),
    url(r'^prod/$', views.ShopProdView.as_view(), name='prod'),
    url(r'^inven/$', views.ShopInvenView.as_view(), name='inven')

]
