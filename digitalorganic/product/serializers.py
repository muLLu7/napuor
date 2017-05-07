from rest_framework import serializers
from .models import Product,Category



class ProductDetailSerializer(serializers.ModelSerializer):
	#variation_set = VariationSerializer(many=True, read_only=True)
	image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"id",
			"brand",
			"category",
			"sku",
			"pack",
			"unit",
			"code",
			"MRP",
			"expiry",
			"case",
			"image",
			"description",
			"price",
			"active",
			#"variation_set",
		]
	def get_image(self, obj):
		request = self.context.get('request')
		try:
			return request.build_absolute_uri(obj.image.url)
		except:
			return None


class ProductSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='product_detail')
	image = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()
	#variation_set = VariationSerializer(many=True)
	#image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"id",
			"brand",
			"sku",
			"category",
			"pack",
			"unit",
			"price",
			#"expiry",
			"image",
			#"active",
			"url",
			#"variation_set",
		]
	
	def get_image(self, obj):
		request = self.context.get('request')
		try:
			return request.build_absolute_uri(obj.image.url)
		except:
			return None
	
	def get_price(self, obj):
		request = self.context.get('request')
		try:
			return obj.get_price()
		except:
			return None
			

class CategorySerializer(serializers.ModelSerializer):
	#variation_set = VariationSerializer(many=True, read_only=True)
	image = serializers.SerializerMethodField()
	class Meta:
		model = Category
		fields = [
			"id",
			"title",
			"image",
			#"variation_set",
		]
	def get_image(self, obj):
		request = self.context.get('request')
		try:
			return request.build_absolute_uri(obj.image.url)
		except:
			return None
		