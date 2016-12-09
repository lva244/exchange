from django.conf.urls import url

from . import views

app_name = 'exchange'
urlpatterns = [
    url(r'^$', views.ExchangePage.as_view(), name='form'),
    url(r'^getid/$', views.GetIdPage.as_view(), name='getid'),
    url(r'^exchange_like/admin/import/$', views.ImportPage.as_view(), name='import'),
    url(r'^barcode/import/$', views.BarCodePage.as_view(), name='barcode'),
]