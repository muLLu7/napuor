from rest_framework import serializers
from django.contrib.auth import models
from django.contrib.auth import get_user_model,authenticate # If used custom user model
from django.core.mail import send_mail

from django.contrib.auth.models import User, Group

from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers,exceptions
from rest_auth.models import TokenModel
from .models import Account
from django.http import JsonResponse,HttpResponse
UserModel = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
	#password = serializers.CharField(write_only=True)
	#confirm_password = serializers.CharField(write_only=True)
	
	class Meta:
		model = UserModel
		fields = ('url','username','first_name','last_name','email')
		#fields = ('url','username','first_name','last_name','email')
	'''    
	def create(self,validated_data):
		self.validate(validated_data)
		user = UserModel.objects.create(
				username=validated_data['username'],
				email=validated_data['email'],
				)    
		user.set_password(validated_data['password'])
		user.save()
		self.custom_signup(validated_data)
		return user

	def validate(self, data):
		if data['password'] != data['confirm_password']:
			raise serializers.ValidationError(("The two password fields didn't match."))
		
		return data

	def custom_signup(self,validated_data):
		to_mail = ['napuor@gmail.com']
		to_mail.append(str(self.validated_data['email']))
		send_mail('Registration Successful','Explore the Natural Pure Organic World','napuor@gmail.com',to_mail)
  
	'''    


class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = UserModel
		#fields = ('url','username','first_name','last_name','email')

	
	def update(self, instance, validated_data):
		instance.username = validated_data.get('username', instance.username)
		instance.email = validated_data.get('email', instance.email)
		#instance.password = validated_data.get('password', instance.password)
		#user.set_password(validated_data['password'])
		self.validate(validated_data)
		#instance.set_password(validated_data['password'])
		instance.save()
		return instance    


class UsersSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = UserModel
		fields = ('url','id','username','email')

	def update(self, instance, validated_data):
		instance.username = validated_data.get('username', instance.username)
		instance.email = validated_data.get('email', instance.email)
		#instance.password = validated_data.get('password', instance.password)
		#user.set_password(validated_data['password'])
		self.validate(validated_data)
		#instance.set_password(validated_data['password'])
		instance.save()
		return instance    
  
class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')


class PasswordResetSerializer(serializers.Serializer):
	"""
	Serializer for requesting a password reset e-mail.
	"""
	email = serializers.EmailField()
	


class  AccountListSerializer(serializers.ModelSerializer):
	#url= serializers.CharField(source='user.url')
	username = serializers.CharField(read_only=True,source='user.username')
	first_name= serializers.CharField(source='user.first_name')
	last_name= serializers.CharField(source='user.last_name')
	email=serializers.CharField(source='user.email')
	#user_id = serializers.CharField(source='user.id')
	customer_id = serializers.CharField(source='id',read_only=True)

	#email= serializers.CharField(source='User.email')
	class Meta:
		model = Account
		'''
		fields = ( 'customer_id','username','first_name','last_name','email','street_address1','street_address2',
		 'city', 'state','pincode', 'phone')
		'''
		fields = ( 'customer_id','username','first_name','last_name','email','pincode', 'phone')
		
		read_only_fields=('customer_id',)
	
	def update(self, instance, validated_data):
		#instance.user.email = validated_data.get('user', instance.user).get('email')
		email = validated_data.get('user', instance.user).get('email')
		if email != instance.user.email:
			try:
				usr = UserModel.objects.get(email=email)
				raise serializers.ValidationError(("E-mail is already used"))
			except UserModel.DoesNotExist:
				instance.user.email = validated_data.get('user', instance.user).get('email')
		instance.user.first_name = validated_data.get('user', instance.user).get('first_name')
		instance.user.last_name = validated_data.get('user', instance.user).get('last_name')
		#instance.street_address1 = validated_data.get('street_address1', instance.street_address1)
		#instance.street_address2 = validated_data.get('street_address2', instance.street_address2)
		#instance.city = validated_data.get('city', instance.city)
		#instance.state = validated_data.get('state', instance.state)
		instance.phone = validated_data.get('phone', instance.phone)
		instance.pincode = validated_data.get('pincode', instance.pincode)
		#print(validated_data)
		##print(validated_data[user].email)
		#print(instance.user.email)
		#customer=Account.objects.get(id=instance.customer_id)
		#user= User.object.get(id=customer.user.id)
		#user.email=instance.email
		#user.save()
		#instance.street_address1 = validated_data.get('street_address1', instance.street_address1)
		#self.validate(validated_data)
		

		#instance.set_password(validated_data['password'])
		instance.user.save()
		instance.save()
		return instance    


class AccountCreateSerializer(serializers.ModelSerializer):
	#url= serializers.CharField(source='user.url')
	username = serializers.CharField(write_only=True)
	email= serializers.CharField(write_only=True)
	first_name= serializers.CharField(write_only=True)
	last_name= serializers.CharField(write_only=True)
	
	password = serializers.CharField(write_only=True)
  
	confirm_password = serializers.CharField(write_only=True)
	customer_id = serializers.CharField(read_only=True)
	class Meta:
		model = Account
		'''
		fields = ( 'customer_id','username','email','password','confirm_password','first_name','last_name','street_address1','street_address2',
		 'city', 'state','pincode', 'phone')
		'''
		fields = ( 'customer_id','username','email','password','confirm_password','first_name','last_name','pincode', 'phone')
		
		read_only_fields = ('customer_id',)
	def create(self,validated_data):
		self.validate(validated_data)
		user = UserModel.objects.create(
				username=validated_data['username'],
				email=validated_data['email'],
				first_name=validated_data['first_name'],
				last_name=validated_data['last_name'],
				)    
		user.set_password(validated_data['password'])
		user.save()
		act = Account.objects.create(
				user=user,
				#street_address1=validated_data['street_address1'],
				#street_address2=validated_data['street_address2'],
				#city=validated_data['city'],
				#state=validated_data['state'],
				phone=validated_data['phone'],
				pincode=validated_data['pincode'],
			)
		self.custom_signup(validated_data)
	
		return act
	
	def update(self, instance, validated_data):

		return instance


	def validate(self, data):
		if data['password'] != data['confirm_password']:
			raise serializers.ValidationError(("The two password fields didn't match."))
		
		email = data['email']
		try:
			usr = UserModel.objects.get(email=email)
			raise serializers.ValidationError(("E-mail is already used"))
		except UserModel.DoesNotExist:
			usr = None	
		username = data['username']
			
		try:
			usr = UserModel.objects.get(username=username)
			raise serializers.ValidationError(("username taken"))
		except UserModel.DoesNotExist:
			usr = None	

		return data
	
	def custom_signup(self,validated_data):
		to_mail = ['napuor@gmail.com']
		to_mail.append(str(self.validated_data['email']))
		send_mail('Registration Successful','Explore the Natural Pure Organic World','napuor@gmail.com',to_mail)
	

class MyLoginSerializer(serializers.Serializer):
    #username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        user = None
        print(email)
        print(password)
       
        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    
    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user     

    def validate(self, attrs):
        #username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        usr = UserModel.objects.get(email=email)
        #user = self._validate_email(email, password)
        user = self._validate_username(usr.username, password)
        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        
        attrs['user'] = user
        return attrs



class MyTokenSerializer(serializers.ModelSerializer):
	"""
	Serializer for Token model.
	"""
	user_id=serializers.SerializerMethodField()
	customer_id=serializers.SerializerMethodField()

	class Meta:
		model = TokenModel
		fields = ('user_id','customer_id','key',)        

	def get_user_id(self, obj):
		request = self.context.get('request')
		try:
			return request.user.id
		except:
			return None
	
	def get_customer_id(self, obj):
		request = self.context.get('request')
		try: 
			customer = Account.objects.get(user=request.user)
		
		except Account.DoesNotExist:
			return None    
		
		try:
			return customer.id
		except:
			return None
			 