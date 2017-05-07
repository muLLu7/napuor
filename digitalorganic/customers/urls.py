
from django.conf.urls import include, url
from .views import  (UserRegistration,CustomerAccountCreateView,
	CustomerAccountListView,CustomerDetail)
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
#from rest_auth.registration.views import RegisterView



urlpatterns = [
    url(r'^$', CustomerDetail.as_view(),name='account_details'),
    url(r'^register/$', CustomerAccountCreateView.as_view(),name='account_signup'),
    
 ]
