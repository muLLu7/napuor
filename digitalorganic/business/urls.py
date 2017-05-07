from django.conf.urls import patterns, url
from .views import (
					BannerListAPIView,BannerRetrieveAPIView,
					pincode_view,statelist_view,
					place_view,
					EnquiryList,
					order_enquiry,
					)

urlpatterns = patterns(
	'business.views',
	url(r'^banners/$',BannerListAPIView.as_view(), name='banner_list'),
	url(r'^banners/(?P<pk>\d+)/$', BannerRetrieveAPIView.as_view(), name='banner_detail'),
    url(r'^pincode/(?P<pk>\d+)/$', pincode_view, name='pincode_place'),
	url(r'^states/$', statelist_view, name='states'),
	url(r'^place/(?P<place>.+?)/$', place_view, name='place_detail'),
	url(r'^enquiry/$',EnquiryList.as_view(), name='enquiry'),
	url(r'^organic/$',order_enquiry, name='order_enquiry'),
	#url(r'^enquiries/$',OrderEnquiryList.as_view(), name='order_enquiry_list'),
	
	)

	#url(r'^api/products/$', ProductListAPIView.as_view(), name='products_api'),
	#url(r'^api/products/(?P<pk>\d+)/$', ProductRetrieveAPIView.as_view(), name='products_detail_api'),
