from cart.models import Cart, CartItem,Order
from django.core.exceptions import ValidationError
from django.core import serializers
from django.contrib.auth.decorators import login_required

from product.models import Product
from customers.models import Account
from cart.serializers import CartSerializer, CartItemSerializer,OrderSerializer
from rest_framework import generics
from rest_framework import permissions
# Needed for AddCartItem view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer

from django.views.generic.base import View
from django.core import serializers
from django.http import HttpResponseRedirect, Http404, HttpResponse,JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.core.mail import send_mail


class CartItemList(generics.ListCreateAPIView):
	model = CartItem
	serializer_class = CartItemSerializer
	permission_classes = (permissions.IsAuthenticated,)
	
	def get_queryset(self):
		#print(self.request.user)
		try:
			customer = Account.objects.get(user=self.request.user)
			#print(customer)
		except Account.DoesNotExist:
			#return JsonResponse({'error':'Enter valid account id / cart id'},status=400)	
			return None
		try:
			customer_cart =  Cart.objects.get(customer=customer)
			#print(customer_cart)
		except Cart.DoesNotExist:
			customer_cart = None
			return None

		if 	customer_cart is not None:
			try:
				queryset = CartItem.objects.filter(cart=customer_cart)
			except CartItem.DoesNotExist:
				return JsonResponse({'error':'Cart does not exist'},status=400)
			return queryset	
		
	'''
	def get(self, request, format=None):
	
		qs = self.get_queryset()
		serializer = CartItemSerializer(qs)
		if qs is not None:
			return Response(serializer.data)
		else:    
			return JsonResponse({'error':'Cart does not exist'},status=400)
	'''		

	def post(self, request, *args, **kwargs):
		#self.get_queryset()	
		##print(request.data)
		count = Product.objects.count()

		try:
			customer = Account.objects.get(user=request.user)
		except Account.DoesNotExist:
			return JsonResponse({'error':'Enter valid account id / cart id'},status=400)	

		##print(customer)
		try:
			customer_cart =  Cart.objects.get(customer=customer)
		except Cart.DoesNotExist:
			return JsonResponse({'error':'Cart does not exist. create cart/'},status=400)	
				
		##print(customer_cart)
		if str(customer_cart.id) == str(request.data['cart']):
			try:
				cart= Cart.objects.get(customer=customer)
				#print(cart)
			except Cart.DoesNotExist:
				return JsonResponse({'error':'Cart does not exist'},status=400)
			

			if cart is not  None:
				#print(request.data)
				if int(request.data['quantity']) <= 0: 
					return JsonResponse({'error':'Invalid Qunatity. Need positive integer'},status=400)
				if (request.data['product']) is not None:
					#print(request.data['product'])
					#print(request.data['quantity'])
					try:
						prod  = CartItem.objects.get(cart=customer_cart,product=request.data['product'])
					except CartItem.DoesNotExist:
						prod = None
					#print(prod)
					if prod is not None:
						prod.quantity += int(request.data['quantity'])
						request.data['quantity'] = prod.quantity
						prod.save()
						serializer = CartItemSerializer(prod,data=request.data)
						#response = json.dumps(prod,cls=DjangoJSONEncoder)
						#return self.list(request, *args, **kwargs)
						if serializer.is_valid():	
							return JsonResponse(serializer.data)
						return JsonResponse({'error':'Data error'},status=400)		  
					if int(request.data['product']) <= count and int(request.data['product']) > 0  :
						serializer = CartItemSerializer(cart,data=request.data)
						return self.create(request, *args, **kwargs)
					else: 
						return JsonResponse({'error':'Product ID out of range'},status=400)	
				else:
					return JsonResponse({'error':'Product ID cannot be NULL'},status=400)	
							
				
				if (request.data['quantity']) is not None:	
					#print((request.data['quantity']))	
					if request.data['quantity'] >  0  :
						serializer = CartItemSerializer(cart,data=request.data)
						return self.create(request, *args, **kwargs)
					else: 
						return JsonResponse({'error':'Quantity needs to be a positive interger'},status=400)	
				else:
					return JsonResponse({'error':'Quantity cannot be NULL'},status=400)	
						

			else:
				return JsonResponse({'error':'Cart Does not Exist'},status=400) 
		else:
				return JsonResponse({'error':'Enter valid cart id for this customer'},status=400)		

class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = CartItem.objects.all()
	serializer_class = CartItemSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		queryset = CartItem.objects.all()
		customer = Account.objects.get(user=self.request.user)
		#print (self.request.user)
		#print (customer)
		customer_cart =  Cart.objects.get(customer=customer)
		#print(customer_cart)
		queryset = queryset.filter(cart=customer_cart)
		return queryset	

class CartList(generics.ListAPIView):
	queryset = Cart.objects.all()
	serializer_class = CartSerializer
	#permission_classes = (permissions.IsAuthenticated,)
	permission_classes = (permissions.IsAdminUser,)
	
	'''
	def get(self, request):
		customer = Account.objects.get(user=request.user)
		#print (request.user)
		#print (customer)
		customer_cart =  Cart.objects.get(customer=customer)
		serializer = CartSerializer(customer_cart)
		return Response(serializer.data)
	
	def get_queryset(self):
		queryset = CartItem.objects.all()
		customer = Account.objects.get(user=self.request.user)
		#print (self.request.user)
		#print (customer)
		customer_cart =  Cart.objects.get(customer=customer)
		#print(customer_cart)
		queryset = queryset.filter(cart=customer_cart)
		return queryset	/
	'''
	

class CartDelete(generics.RetrieveDestroyAPIView):
	#queryset = Cart.objects.all()
	serializer_class = CartSerializer
	permission_classes = (permissions.IsAuthenticated,)
	
	
	def get_queryset(self):
		id = self.request.query_params.get('id', None)
		queryset = Cart.objects.all()
		customer = Account.objects.get(user=self.request.user)
		try:
			queryset = queryset.filter(customer=customer)
		except queryset.DoesNotExist:
			return JsonResponse({'error':'Cart is not created'},status=400)	
		return queryset	
	
	


class CustomerCart(generics.ListCreateAPIView):
	model = Cart
	serializer_class = CartSerializer
	permission_classes = (permissions.IsAuthenticated,)
	
	def get_queryset(self):
		queryset = Cart.objects.all()
		try:
			customer = Account.objects.get(user=self.request.user)
		except Account.DoesNotExist:
			return JsonResponse({'error':'Invalid Account'},status=400)	
		
		try:
			customer_cart = Cart.objects.filter(customer=customer)
			return customer_cart
	
		except Cart.DoesNotExist:
			return JsonResponse({'error':'Cart is not created. Create using cart/create'},status=400)	

		#queryset = queryset.filter(customer=customer)
		
		#return queryset	
	
	
	def post(self, request, *args, **kwargs):
			
		try:
			customer = Account.objects.get(id=request.data['customer'])
		except Account.DoesNotExist:
			return JsonResponse({'error':'Invalid customer ID',},status=400)
		if str(customer) ==  str(request.user) :
			#print('same')
			try:
				cart= Cart.objects.get(customer=customer)
			except Cart.DoesNotExist:
				#raise Http404
				cart = None
			#print(cart) 
			if cart is  None:
				#return self.create(request, *args, **kwargs)
				new_Cart = self.create(request, *args, **kwargs)
				return new_Cart
			else:
				return JsonResponse({'error':'Cart Exists'},status=400) 
					
		else:	
			#print('not same')
			return JsonResponse({'error':'Invalid username',},status=400)

  

class OrderDetails(generics.ListCreateAPIView):
	#queryset = Cart.objects.all()
	serializer_class = OrderSerializer
	#permission_classes = (permissions.IsAuthenticated,)
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		try:
			customer = Account.objects.get(user=self.request.user)
		except Account.DoesNotExist:
			return JsonResponse({'Error':'Invalid Customer ID',},status=400)
		queryset = Order.objects.all()
		queryset = queryset.filter(customer=customer)
		return queryset	



	def post(self, request, *args, **kwargs):
		self.get_queryset()

		try:	
			customer = Account.objects.get(id=request.data['customer'])
		except Account.DoesNotExist:
			return JsonResponse({'Error':'Invalid Customer ID',},status=400)
				
		#print(customer)
		#print(request.user)
		if str(customer) ==  str(request.user) :
			#print('same')
			try:
				cart= Cart.objects.get(customer=customer)
				if cart is not None:
					if cart.get_items_count() == 0:
						return JsonResponse({'Error':'Cart Empty',},status=400)
		
					customer_name =  customer.user.first_name+"  "+customer.user.last_name
					customer_email = customer.user.email
					customer_phone= customer.phone
					
					order_items = cart.cart_items
					#print(order_items)
					tax = cart.tax
					shipping = cart.shipping
					order_total = cart.total_price
					order = Order.objects.create(customer=customer,name=customer_name,
						phone=customer_phone,email=customer_email,pincode=request.data['pincode'],
						house=request.data['house'],street=request.data['street'],
						place=request.data['place'],city=request.data['city'],
						state=request.data['state'],order_items=order_items,tax=tax,
						shipping=shipping,order_total=order_total)	
					
					ord_message =	 "Thank You for submitting Order Enquiry" + "\n"
	
					ord_message +=    str(customer_name) + '\n'
					ord_message +=    str(customer_phone) + '|'
					ord_message +=    str(customer_email) + '|'
					ord_message +=    str(order.pincode) + '\n'
					ord_message +=    '--------------------------------------------------------------------' + '\n'
					
					ord_message +=    'Item List' + '\n'
					ord_message +=    '--------------------------------------------------------------------' + '\n'
					ord_items = CartItem.objects.filter(cart=cart)
					#print(ord_message)
					order_total = 0
					for e in ord_items:
						ord_message += (e.product.sku + ' Quantity: '+ str(e.quantity) + 
										' Price: '+str(e.line_item_total)+'\n')  
						order_total += e.line_item_total
					
					ord_message +=    '--------------------------------------------------------------------' + '\n'
						
					ord_message +=    'Order Total: ' + str(order_total) +'\n'		  
					ord_message +=    'Tax: ' + str(cart.tax) +'\n'		  
					ord_message +=    'Shipping: ' + str(cart.shipping) +'\n'		  
					ord_message +=    '--------------------------------------------------------------------' + '\n'
					ord_message +=    'Total: ' + str(cart.total_price) +'\n'		  
										


					to_mail = ['napuor@gmail.com']
					to_mail.append(str(cart.customer.user.email))
					send_mail('Order Complete',ord_message,'napuor@gmail.com',to_mail)
					cart.delete()

			except Cart.DoesNotExist:
				return JsonResponse({'Error':'There is no active Cart for this user',},status=400)

			#return self.create(request, *args, **kwargs)
			return JsonResponse({'Success':'Order Complete',},status=200) 
					
		else:	
			return JsonResponse({'error':'Invalid Customer ID',},status=400)
 
PAYMENT_MODE=(
    ("POD","Payment On Delivery"),
    ("ONLINE", "On-line Banking"), 
    ("CARD", "Card Payment"),
    )  

def payment_mode(request):
	data = {
			"POD": "Payment On Delivery",
			"ONLINE": "On-line Banking",
			"CARD": "Card Payment",
			}

	return JsonResponse(data,status=200) 
