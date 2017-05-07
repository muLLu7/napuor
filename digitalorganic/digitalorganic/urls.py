"""digitalorganic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns

from customers.views import (UsersViewSet,GroupViewSet,UserRegistration,
							CustomersViewSet,MyLoginView,PasswordResetView)
from business.views import APIHomeView,order_enquiry,home
from rest_framework import routers
from rest_auth.views import (
	LogoutView,PasswordChangeView,
)
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
import rest_auth

admin.autodiscover()



router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'groups', GroupViewSet)

#router.register(r'customers', CustomersViewSet.as_view)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
#http://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html

	

urlpatterns = [
	url(r'^$', home, name='home'),
	url(r'^about/$', 'business.views.about', name='about'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^business/', include('business.urls')),
	url(r'^products/', include('product.urls')),
	url(r'^cart/', include('cart.urls')),
	url(r'^api/$', APIHomeView.as_view()),
	url(r'^account/', include('customers.urls')),
	url(r'^login/$', MyLoginView.as_view(), name='account_login'),
	url(r'^logout/$', LogoutView.as_view(), name='user_logout'),
	url(r'^password/reset/$', PasswordResetView.as_view(),
		name='user_password_reset'),
	url(r'^password/change/$', PasswordChangeView.as_view(),
		name='user_password_change'),
	
]


'''
if settings.SERVE_MEDIA:
	urlpatterns += patterns("",
		(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
		) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


if settings.SERVE_MEDIA:
	urlpatterns += patterns("",
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.STATIC_ROOT,'show_indexes': True}),
		) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
'''

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)