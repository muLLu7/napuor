from django.shortcuts import render
from django.core import serializers
from rest_framework.renderers import JSONRenderer

from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,RetrieveAPIView
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Product,Category
from .serializers import ProductSerializer,ProductDetailSerializer,CategorySerializer
from .filters import ProductFilter
from django.http import HttpResponseRedirect, Http404, HttpResponse,JsonResponse

# Create your views here.




def category_list(request):
	queryset = Product.objects.values_list('category').order_by('category')
	queryset = sorted(set(queryset))
	serialized_q = json.dumps(list(queryset), cls=DjangoJSONEncoder)
	return HttpResponse(serialized_q,status=200) 


class CategoryListAPIView(generics.ListAPIView):
	#permission_classes = [IsAuthenticated]
	#queryset = Product.objects.all()
	serializer_class = CategorySerializer
	'''
	filter_backends = [
					filters.SearchFilter, 
					filters.OrderingFilter, 
					filters.DjangoFilterBackend
					]
	search_fields = ["sku", "description"]
	ordering_fields  = ["id","sku"]
	filter_class = ProductFilter
	'''
	def get_queryset(self):
		queryset = Category.objects.all()
		
		return queryset
	
class CategoryRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer



class ProductListAPIView(generics.ListAPIView):
	#permission_classes = [IsAuthenticated]
	#queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [
					filters.SearchFilter, 
					filters.OrderingFilter, 
					filters.DjangoFilterBackend
					]
	search_fields = ["sku", "description"]
	ordering_fields  = ["id","sku"]
	filter_class = ProductFilter

	# Show all of the PASSENGERS in particular WORKSPACE
	# or all of the PASSENGERS in particular AIRLINE
	def get_queryset(self):
		queryset = Product.objects.all()
		sku = self.request.query_params.get('sku', None)
		category = self.request.query_params.get('category', None)

		if sku is not None:
			queryset = queryset.filter(sku__icontains=sku)
		elif category is not None:
			queryset = queryset.filter(category__icontains=category)

		return queryset
	

class ProductRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer


class ProductDetail(RetrieveAPIView):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	model = Product
	serializer_class = ProductSerializer
	#permission_classes = (IsAuthenticated,)
	#authentication_classes = (TokenAuthentication,) 

	
	def get_object(self, pk):
		try:
			return Product.objects.get(product_id=pk)
		except Product.DoesNotExist:
			return None

	def get(self, request, pk, format=None):
		act = self.get_object(pk)
		serializer = ProductSerializer(act)
		if act is not None:
			return Response(serializer.data)
		else:    
			return Response(status=status.HTTP_204_NO_CONTENT)
	def put(self, request, pk, format=None):
		act = self.get_object(pk)
		serializer = ProductSerializer(act, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		act = self.get_object(pk)
		act.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


'''
@api_view(['GET','POST'])
def product_list(request):
	"""
	List All Products or create a new product
	curl http://localhost/products/
	curl -X POST http://localhost/products/ -d "no=1&title=orange&price=100" 
	"""
	if request.method == 'GET':
		products = Product.objects.all()
		serializer = ProductSerializer(products,many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def product_detail(request,pk):
	"""
	Get, Update or Delete a particular product
	curl -X PUT http://localhost/api/products/1 -d "no=1&title=orange&price=100"
	curl -X PUT http://localhost/api/products/1 -d "no=1&title=orange"
	curl -X DELETE http://localhost/api/products/1
	"""
	try:
		product = Product.objects.get(pk=pk)
	except Product.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = ProductSerializer(product)
		return Response(serializer.data)
	elif request.method == 'PUT':
		serializer = ProductSerializer(product,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		product.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)						
'''