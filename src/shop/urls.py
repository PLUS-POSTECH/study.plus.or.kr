from django.conf.urls import url

from shop import views

app_name = 'shop'

urlpatterns = [
    url(r'^(?P<pk>\d+)/buy$', views.ShopPurchaseView.as_view(), name='buy'),
    url(r'^(?P<pk>\d+)$', views.ShopProdView.as_view(), name='prod'),
    url(r'^$', views.ShopProdView.as_view(), name='prod'),
    url(r'^inven/$', views.ShopInvenView.as_view(), name='inven'),
    url(r'^/retrieve/(?P<pk>\d+)$', views.ShopRetrieveView.as_view(), name='retrieve')
]
