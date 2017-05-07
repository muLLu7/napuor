from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (CartList,CustomerCart,CartDelete,
		CartItemList,CartItemDetail,OrderDetails,payment_mode)

urlpatterns = patterns('cart.views',
    #url(r'^$', CartList.as_view()),
    url(r'^$', CustomerCart.as_view(),name='my_cart'),
    url(r'^order/$', OrderDetails.as_view(),name='my_order'),
    #url(r'^order/create$', OrderCreate.as_view(),name='order_create'),
    #url(r'^create/$', CartCreate.as_view(),name='cart_create'),
    url(r'^(?P<pk>[0-9]+)/$', CartDelete.as_view(),name='cart_delete'),
    url(r'^items/$', CartItemList.as_view(),name='items'),
    url(r'^items/(?P<pk>[0-9]+)/$', CartItemDetail.as_view(),name='item'),
    url(r'^paymentmode/$', payment_mode,name='payment_mode'),
    
    #url(r'^(?P<pk>[0-9]+)/additems/$', AddCartItem.as_view()),
    #url(r'^cartitems/$', CartItemList.as_view(), name='cartitem-list'),
    #url(r'^cartitems/(?P<pk>[0-9]+)/$', CartItemDetail.as_view(), name='cartitem-detail'),
)

#urlpatterns = format_suffix_patterns(urlpatterns)
