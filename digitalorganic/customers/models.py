from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator 

#models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True) #not required

class Account(models.Model):
	#date_created = models.DateTimeField(auto_now_add=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='+')
	#street_address1 = models.CharField(max_length=255)
	#street_address2 = models.CharField(max_length=255, blank=True, null=True)
	#city = models.CharField(max_length=255)
	#state = models.CharField(max_length=255)
	pincode = models.PositiveIntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)],blank=True)
	phone = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)],blank=True)	

	def __str__(self):
		return self.user.username 
