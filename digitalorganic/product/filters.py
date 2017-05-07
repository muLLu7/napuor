from django_filters import FilterSet, CharFilter, NumberFilter

from .models import Product

class ProductFilter(FilterSet):
	sku = CharFilter(name='sku', lookup_type='icontains', distinct=True)
	category = CharFilter(name='category', lookup_type='icontains', distinct=True)
	price = NumberFilter(name='price', lookup_type='lte', distinct=True) # (some_price__gte=somequery)
	#max_price = NumberFilter(name='variation__price', lookup_type='lte', distinct=True)
	class Meta:
		model = Product
		fields = [
			'price',
			'category',
			'sku',
			]