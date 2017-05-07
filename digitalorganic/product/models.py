from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
from django.utils.text import slugify


# Create your models here.
# Create your models here.

PACK_CHOICES= (
	('UNIT','NUMBERS'),
	('1_KG','1 KG'),
	('2_KG','2 KG'),
	('5_KG','5 KG'),
	('100_GM','100 GM'),
	('150_GM','150 GM'),
	('200_GM','200 GM'),
	('250_GM','250 GM'),
	('500_GM','500 GM'),
	('100_ML','100 ML'),
	('250_ML','250 ML'),
	('500_ML','500 ML'),
	('100_ML','100 ML'),
	('25_BAGS','25 BAGS'),
	('1_LT','1 LT'),
	('KG_100','QUINTAL'),
	('QUINTAL_10','TON'),
	('DOZEN','DOZEN'),	
)


EXPIRY_CHOICES= (
	('3 Months','3 Months'),
	('6 Months','6 Months'),
	('9 Months','9 Months'),
	('12 Months','12 Months'),
	('24 Months','24 Months'),
	('18 Months','18 Months'),
	('4 Months','4 Months'),
)



def image_upload_to(instance, filename):
	title = instance.sku
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s.%s" %(title,file_extension)
	return "products/%s" %(new_filename)

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()

	

class Product(models.Model):
	id = models.AutoField(primary_key=True)
	brand = models.CharField(max_length=50,default='Napuor')
	category= models.CharField(max_length=100,default='Organic')
	sku = models.CharField(max_length=120,default='Organic')
	pack = models.IntegerField(default=1000)
	unit = models.CharField(max_length=10,default='GM')
	code = models.IntegerField(default=1000)
	MRP = models.DecimalField(decimal_places=2,max_digits=20,default=100.00)
	expiry = models.CharField(max_length=50,default='24 Months')
	case = models.IntegerField(default=1000)
	image = models.ImageField(null=True, blank=True,upload_to=image_upload_to)
	description = models.TextField(null=True)
	price = models.DecimalField(decimal_places=2,max_digits=20,default=100.00)
	active = models.BooleanField(default=True)
	
	objects = ProductManager()

	def __str__(self):
		return '%d' % self.id

	def __unicode__(self): 
		return self.sku
		
		

	class Meta:
		ordering = ["id"]
	
	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk": self.pk})
	
	
	def get_image_url(self):
		img = self.image
		
		if img:
			return img.url
		
		return img #None
	
	def get_price(self):
		if self.price != self.MRP:
			return self.price
		else:
			return self.MRP

	def add_to_cart(self):
		return "%s?item=%s&qty=1" %(reverse("cart"), self.id)

	def remove_from_cart(self):
		return "%s?item=%s&qty=1&delete=True" %(reverse("cart"), self.id)

	def get_title(self):
		return "%s" %(self.sku)
			

def cat_image_upload_to(instance, filename):
	return "category/%s" %(filename)


class Category(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50)
	image = models.ImageField(null=True, blank=True,upload_to=cat_image_upload_to)
	
	class Meta:
		verbose_name_plural = "Categories"

	
	def __str__(self):
		return self.title


