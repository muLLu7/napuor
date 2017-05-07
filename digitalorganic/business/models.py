from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator,MinValueValidator 
from product.models import Product
from django.db.models.signals import pre_save, post_save, post_delete
from decimal import Decimal

BANNER_SIZE = (
	("small","small"),
	("medium","medium"),
	("large","large"),
	("medium","ultra"),
	)

def banner_image_upload_to(instance, filename):
	return "banner/%s" %(filename)


# Create your models here.
class Banner(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=120, unique=True)
	small = models.ImageField(null=True, blank=True,upload_to=banner_image_upload_to)
	large = models.ImageField(null=True, blank=True,upload_to=banner_image_upload_to)
	#size = models.CharField(max_length=30,choices=BANNER_SIZE,default="SMALL")
	description = models.TextField(null=True, blank=True)
	#timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	
	#objects = ProductManager()

	class Meta:
		verbose_name_plural = "Banners"

	
	def __str__(self):
		return self.title	

ENQUIRY_STATUS = (
	("INFO_RQUESTED","IR"),
	("RESPONSE_SENT","RS"),
	("QUERY_RESOLVED","QR"),
	)
class Enquiry(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100,blank=True, null= True)
	last_name = models.CharField(max_length=100,blank=True, null= True)
	mobile = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
	email = models.EmailField(max_length=70, unique= False)
	pincode = models.PositiveIntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)])
	info_request = models.TextField(max_length=1000,blank=True, null= True) 
	date_created = models.DateTimeField(auto_now_add=True) 
	date_updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices=ENQUIRY_STATUS,default='IR')

	class Meta:
		verbose_name_plural = "Enquiries"

	def __str__(self):
		return '%d- %s %s' % (self.id,self.first_name,self.last_name)



class EnquiryItem(models.Model):
	id = models.AutoField(primary_key=True)
	contact_query = models.ForeignKey('ContactQuery', on_delete=models.CASCADE)
	product = models.ForeignKey(Product,  on_delete=models.CASCADE,help_text='')
	quantity = models.PositiveIntegerField(default=1, help_text='')
	line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		ordering = ['product']

	def __unicode__(self):
		return u'%i of %s' % (self.quantity, self.product.name)
	def __str__(self):
		return '%s' % (self.product.sku)
	

  
def item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty = int(instance.quantity)
	if qty >= 1:
		price = instance.product.get_price()
		line_item_total = Decimal(qty) * Decimal(price)
		instance.line_item_total = line_item_total
	instance.contact_query.update_subtotal()

pre_save.connect(item_pre_save_receiver, sender=EnquiryItem)

def item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.contact_query.update_subtotal()
   
post_save.connect(item_post_save_receiver, sender=EnquiryItem)

post_delete.connect(item_post_save_receiver, sender=EnquiryItem)


class ContactQuery(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	mobile = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
	email = models.EmailField(max_length=70, unique= False)
	pincode = models.PositiveIntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)])
	#info_request = models.TextField(max_length=1000,blank=True, null= True) 
	items_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	date_created = models.DateTimeField(auto_now_add=True) 
	date_updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices=ENQUIRY_STATUS,default='IR')

	class Meta:
		verbose_name_plural = "ContactEnquiries"

	def __str__(self):
		return '%d- %s %s' % (self.id,self.first_name,self.last_name)

	def update_subtotal(self):
		subtotal = 0
		#items = self.items.all()
		items=EnquiryItem.objects.filter(contact_query=self)

		#print(items)
		for item in items:
			subtotal += item.line_item_total
		self.items_total=subtotal
		#print(self.items_total)
		self.save()

		