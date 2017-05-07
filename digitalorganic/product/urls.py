from django.conf.urls import patterns, url
from .views import ProductListAPIView, ProductRetrieveAPIView,category_list,CategoryListAPIView,CategoryRetrieveAPIView

urlpatterns = [
	#'product.views',
	url(r'^category/$',CategoryListAPIView.as_view(), name='category_list'),
	url(r'^category/(?P<pk>[0-9]+)/$',CategoryRetrieveAPIView.as_view(), name='category_detail'),
	url(r'^$',ProductListAPIView.as_view(), name='product_list'),
	url(r'^(?P<pk>[0-9]+)/$',ProductRetrieveAPIView.as_view(), name='product_detail'),
	]

	#url(r'^api/products/$', ProductListAPIView.as_view(), name='products_api'),
	#url(r'^api/products/(?P<pk>\d+)/$', ProductRetrieveAPIView.as_view(), name='products_detail_api'),
