from rest_framework import serializers
from .models import  Banner,Enquiry
import datetime



class BannerSerializer(serializers.ModelSerializer):
	small = serializers.SerializerMethodField()
	large = serializers.SerializerMethodField()
	
	class Meta:
		model = Banner
		fields = [
			"title",
			"description",
			"small",
			"large",
			#"default_category",
		]	
	def get_small(self, obj):
		request = self.context.get('request')
		try:
			return request.build_absolute_uri(obj.small.url)
		except:
			return None
	def get_large(self, obj):
		request = self.context.get('request')
		try:
			return request.build_absolute_uri(obj.large.url)
		except:
			return None




class EnquirySerializer(serializers.ModelSerializer):
	#order_status = serializers.CharField(max_length=100)
	date_created = serializers.SerializerMethodField()
	date_updated = serializers.SerializerMethodField()   
	class Meta:
		model = Enquiry
		fields = ('id','first_name','last_name','mobile','email',
				'pincode','info_request','date_created','date_updated')
		read_only_fields = ('id','date_created','date_updated')   
	
	def get_date_created(self, obj):
		request = self.context.get('request')

		datetime_str = obj.date_created
		new_datetime_str = datetime_str.strftime('%d/%m/%Y--%H:%M:%S') 	
		return new_datetime_str

	
	def get_date_updated(self, obj):
		request = self.context.get('request')
		datetime_str = obj.date_updated
		new_datetime_str = datetime_str.strftime('%d/%m/%Y--%H:%M:%S') 	
		return new_datetime_str
		