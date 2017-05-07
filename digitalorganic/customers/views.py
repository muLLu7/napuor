from django.contrib.auth.models import  User,Group
from django.contrib.auth import get_user_model # If used custom user model
from django.contrib.auth import (
	login as django_login,
	logout as django_logout
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, Http404, HttpResponse,JsonResponse
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework import authentication
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import generics
from rest_framework.generics import CreateAPIView,ListCreateAPIView,RetrieveAPIView,ListAPIView,RetrieveUpdateAPIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView

#from .serializers import UserSerializer,UsersSerializer,UserRegistrationSerializer,GroupSerializer,CustomerAccountSerializer,CustomerAccountListSerializer
from .serializers import (UserSerializer,UsersSerializer,UserRegistrationSerializer,GroupSerializer,
							AccountListSerializer,MyLoginSerializer,AccountCreateSerializer,MyTokenSerializer,PasswordResetSerializer)
from .models import Account
from rest_auth.views import LoginView
from rest_auth.models import TokenModel
from rest_auth.serializers import LoginSerializer
from collections import OrderedDict
import json
from hashlib import sha1
import string
import random
UserModel = get_user_model()

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase+ string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class PasswordResetView(GenericAPIView):
	"""
	Calls Django Auth PasswordResetForm save method.

	Accepts the following POST parameters: email
	Returns the success/fail message.
	"""
	serializer_class = PasswordResetSerializer
	permission_classes = (AllowAny,)

	def post(self, request, *args, **kwargs):
		# Create a serializer with request.data
		serializer = self.get_serializer(data=request.data)
		#data = json.loads(str(request.body))
		if serializer.is_valid():
			email = serializer.data['email']
			try:
				user = UserModel.objects.get(email=email)
			except UserModel.DoesNotExist:
				return Response(
				{"detail": ("No user record exists matching this e-mail")},
				status=status.HTTP_200_OK
			)		
			serializer.is_valid(raise_exception=True)
			passwd = id_generator() 
			user.set_password(passwd)
			user.save()
			message = 'New Password: '+ passwd + '\n'
			message += '(Please change password using change password option afger first login)'
			to_mail = [user.email]
			send_mail('Password Recovery',message,'napuor@gmail.com',to_mail)
						
			return Response(
				{"detail": ("Password recovery e-mail has been sent.")},
				status=status.HTTP_200_OK
			)
		return Response(
				{"detail": ("Data error")},
				status=status.HTTP_400_BAD_REQUEST
			)


class UserRegistration(CreateAPIView):
	"""
	Register a new user.
	"""
	model = get_user_model()        
	permission_classes = (AllowAny,)
	
	serializer_class = UserRegistrationSerializer



class MyLoginView(LoginView):
	permission_classes = (AllowAny,)
	serializer_class = MyLoginSerializer
	token_model = TokenModel

	def get_response(self):
		serializer_class = MyTokenSerializer

		serializer = serializer_class(instance=self.token,
										  context={'request': self.request})

		return Response(serializer.data, status=status.HTTP_200_OK)

   



class CustomerAccountCreateView(CreateAPIView):
	model = Account
	serializer_class = AccountCreateSerializer
	permission_classes = (AllowAny,) 
	''' 
	def get_queryset(self):
		print(self.request.user)
		if str(self.request.user) == 'AnonymousUser':
			return None
		try:
			customer = Account.objects.filter(user=self.request.user)
			return customer
		except Account.DoesNotExist:
			return JsonResponse({'Error':'Invalid Customer ID',},status=400)

	'''

	def post(self, request, format=None):
		serializer = AccountCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			usr = UserModel.objects.get(username=request.data['username'])
			act = Account.objects.get(user=usr)
			'''
			results = OrderedDict({'customer_id': act.id,'username':act.user.username,
					'First Name':act.user.first_name,'Last Name':act.user.last_name,
					'E-mail':act.user.email,'Mobile':act.phone,
					'Address1':act.street_address1,'Address2':act.street_address2,
					'City':act.city,'State':act.state,'Pincode':act.pincode, })
			'''
			results = {'customer_id': act.id,'username':act.user.username,}
			return Response(results, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			
class CustomerAccountListView(viewsets.ViewSet):
		queryset = Account.objects.all().order_by('user')
		#serializer_class = CustomerAccountListSerializer
		#authentication_classes = (authentication.TokenAuthentication,)
		model = Account
		serializer_class = AccountListSerializer
		permission_classes = (IsAuthenticated,)
		

		def list(self, request):
			queryset = Customer.objects.all()
			serializer = AccountListSerializer(queryset, many=True,context={'request': request})
			return Response(serializer.data)

		def retrieve(self, request, pk=None):
			useract = Customer.objects.get(user_id=pk)
			#user = get_object_or_404(queryset, user_id=pk)
			serializer = AccountListSerializer(useract)
			return Response(serializer.data)


class CustomerDetail(ListAPIView):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	#http_method_names = [u'get',]
	model = Account
	serializer_class = AccountListSerializer
	permission_classes = (IsAuthenticated,) 
	#authentication_classes = (TokenAuthentication,) 
	
	
	def get_queryset(self):
		try:
			customer = Account.objects.filter(user=self.request.user)
			return customer
		except Account.DoesNotExist:
			return JsonResponse({'Error':'Invalid Customer ID',},status=400)

		
				
		 
	def put(self, request):
		try:
			customer = Account.objects.get(user=request.user)
			act_serializer = AccountListSerializer(customer,data=request.data)
			#return Response(serializer.data)
			if act_serializer.is_valid():
				act_serializer.save()
				return Response(act_serializer.data)
			return Response(act_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		except Account.DoesNotExist:
			return JsonResponse({'error':'Customer is not created.'},status=400)	
			



class UserDetailView(RetrieveAPIView):
	#queryset = UserModel.objects.all()
	model = UserModel
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated,)

	def get_object(self, pk):
		try:
			return UserModel.objects.get(user_id=pk)
		except UserModel.DoesNotExist:
			return None

	def get(self, request, pk, format=None):
		usr = self.get_object(pk)
		serializer = UserSerializer(usr)
		if usr is not None:
			return Response(serializer.data)
		else:    
			return Response(status=status.HTTP_204_NO_CONTENT)

	def put(self, request, pk, format=None):
		usr = self.get_object(pk)
		serializer = UserSerializer(usr, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


		

class UsersViewSet(viewsets.ModelViewSet):
	queryset = UserModel.objects.all()
	serializer_class = UsersSerializer
	permission_classes = (IsAdminUser,)

 
class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = (IsAdminUser,)


class CustomersViewSet(viewsets.ModelViewSet,CreateAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountCreateSerializer
	permission_classes = (AllowAny,)
	
	'''
	@detail_route(methods=['post','get'])
	def get_object(self, pk):
		try:
			return Customer.objects.get(user_id=pk)
		except Customer.DoesNotExist:
			return None


	def post(self, request,pk, **kwargs):

		user = self.get_object(pk)

		self.queryset         = Customer.objects.all()
		self.serializer_class = AccountCreateSerializer

		serializer = AccountCreateSerializer(act, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	'''
	




