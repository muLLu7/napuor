from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.reverse import reverse as api_reverse
from product.models import Product
from rest_framework.response import Response
from .serializers import BannerSerializer,EnquirySerializer
from .models import Banner,Enquiry,ContactQuery,EnquiryItem
from product.models import Product,Category
from .filters import BannerFilter
from .forms import ContactForm,OrderForm
import requests
from django.http import HttpResponseRedirect, Http404, HttpResponse,JsonResponse
from rest_framework import permissions
from django.core.mail import send_mail
from django.contrib import messages
from digitalorganic import settings



# Create your views here.

	

class APIHomeView(APIView):
	# authentication_classes = [SessionAuthentication]
	# permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		data = {
			"business": {
				"banners": api_reverse("banner_list", request=request),
				
				#"product_details": api_reverse("product_detail", request=request),
			},
			"products": {
				"count": Product.objects.all().count(),
				"products": api_reverse("product_list", request=request),
				"categories": api_reverse("category_list", request=request),
				#"product_details": api_reverse("product_detail", request=request),
			},
			"registration": {
				"user_registration":  api_reverse("account_signup", request=request),				 				
			},
			"cart": {
				"cart": api_reverse("my_cart", request=request),
				#"create_cart": api_reverse("cart_create", request=request),
				#"delete_cart": api_reverse("cart_delete", request=request),
				"cart_items": api_reverse("items", request=request),
				#"cart_item_details": api_reverse("item", request=request),
				"order": api_reverse("my_order", request=request),
				#"order_create": api_reverse("order_create", request=request),

			},
			"authentication": {
				"user_login":  api_reverse("account_login", request=request),
				"user_logout":  api_reverse("user_logout", request=request), 
				"password_reset":  api_reverse("user_password_reset", request=request), 
				"password_change":  api_reverse("user_password_change", request=request),
				"password_reset_confirm":  api_reverse("user_password_reset_confirm", request=request),
				"password_change":  api_reverse("user_password_change", request=request),
			},
			"account": {
				"account_info":   api_reverse("account_details", request=request),
			},
			
			
		}
		return Response(data)

class BannerListAPIView(generics.ListAPIView):
	serializer_class = BannerSerializer
	
	def get_queryset(self):
		queryset = Banner.objects.all()
		
		return queryset
	

	
class BannerRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Banner.objects.all()
	serializer_class = BannerSerializer


'''
	https://data.gov.in/api/datastore/resource.json?resource_id=7eca2fa3-d6f5-444e-b3d6-faa441e35294&api-key=c710a0983e3751fd86fd52ca9fab0417
	key = c710a0983e3751fd86fd52ca9fab0417	
'''

'''
	https://www.whizapi.com/open-api/api-details?id=19
	key = jt91xcmu8w1t8i3njksee2c1
'''

def pincode_view(request,pk):
	url ='https://www.whizapi.com/api/v2/util/ui/in/indian-city-by-postal-code?project-app-key=jt91xcmu8w1t8i3njksee2c1&pin='
	query_url = str(url+pk) 
	r = requests.get(query_url)
	json = r.json()
	#print(json)
	#return Response(json)
	return JsonResponse(json)

def statelist_view(request):
	
	url='https://www.whizapi.com/api/v2/util/ui/in/indian-states-list?project-app-key=jt91xcmu8w1t8i3njksee2c1' 

	query_url = str(url) 
	r = requests.get(query_url)
	json = r.json()
	#print(json)
	#return Response(json)
	return JsonResponse(json)

def place_view(request,place):
	url = 'https://www.whizapi.com/api/v2/util/ui/in/indian-postal-codes?project-app-key=jt91xcmu8w1t8i3njksee2c1&search='
	query_url = str(url+place) 
	r = requests.get(query_url)
	json = r.json()
	#print(json)
	#return Response(json)
	return JsonResponse(json)


class EnquiryList(generics.CreateAPIView):
	queryset = Enquiry.objects.all()
	serializer_class = EnquirySerializer
	permission_classes = (permissions.AllowAny,)

  
def home(request):
	product = Product.objects.all()
	cat = Category.objects.all()
	cnt = Product.objects.count()
	
	context = {
			"product":product,
			"category":cat,
			"cnt":cnt,
		
		}
		
	
	return render(request, "index.html",context)
	#return render(request, "test.html")

def order_enquiry(request):
	title = 'Order Enquiry Form'
	title_align_center = True
	sender = ''
	order_query = ContactQuery()
	product = Product.objects.all()
	cnt = Product.objects.count()
	cat = Category.objects.all()

	if request.GET:
		product = Product.objects.filter(sku__icontains=request.GET.get('q',""))
		cnt = product.count()
	
	if request.POST:
			order_query.first_name= request.POST.get('first_name', "")
			order_query.last_name = request.POST.get('last_name', "")
			order_query.mobile = request.POST.get('mobile', "")
			order_query.pincode = request.POST.get('pincode', "")
			order_query.email = request.POST.get('email', "")
			order_query.save()
			for index,item in enumerate(product):
				count_index = 'my-itm-val_'+str(index+1)
				itm_cnt = request.POST.get(count_index, "")
				if itm_cnt != "":
					if  int(itm_cnt) > 0:
						enquiry_item = EnquiryItem()
						enquiry_item.contact_query = order_query
						enquiry_item.product=item
						enquiry_item.quantity=itm_cnt
						enquiry_item.save()
			sender = order_query.first_name + "  " +order_query.last_name
			subject = 'Order Form Info Request'
			from_email = order_query.email
			to_email = [from_email, 'info@napuor.com']
			to_email.append('archana@napuor.com')
			to_email.append('priyabrata@napuor.com')
			
			order_enquiry_form = order_query 
			enquiry_list= EnquiryItem.objects.filter(contact_query=order_query)
			#print(enquiry_list)
			ord_message =	 "Thank You for submitting Order Enquiry" + "\n"
			
			ord_message +=    str(order_query.first_name)  + str(order_query.last_name) + '\n'
			ord_message +=    str(order_query.mobile) + '|'
			ord_message +=    str(order_query.email) + '|'
			ord_message +=    str(order_query.pincode) + '\n'
			ord_message +=    '--------------------------------------------------------------------' + '\n'
			
			ord_message +=    'Item List' + '\n'
			ord_message +=    '--------------------------------------------------------------------' + '\n'
			
			#print(ord_message)
			order_total = 0
			for e in enquiry_list:
				ord_message += (e.product.sku + ' Quantity: '+ str(e.quantity) + 
								' Price: '+str(e.line_item_total)+'\n')  
				order_total += e.line_item_total
			
			ord_message +=    '--------------------------------------------------------------------' + '\n'
				
			ord_message +=    'Order Total: ' + str(order_total) +'\n'		  
			send_mail(subject,str(ord_message),from_email,to_email)
			
			context = {
			"title": title,
			"title_align_center": title_align_center,
			"enquiry_list":enquiry_list,
			"order_enquiry_form":order_enquiry_form,
			}
		
			return render(request, "response-order-form.html", context)



	context = {
			"title": title,
			"title_align_center": title_align_center,
			"product":product,
			"category":cat,
			"cnt":cnt,		
	    }
		
	return render(request, "enquiry.html", context)

	
def about(request):
	return render(request, "about.html")



	
	