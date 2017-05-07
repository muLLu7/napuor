from django_filters import FilterSet, CharFilter, NumberFilter

from .models import Banner

'''
filters.LOOKUP_TYPES = [
    ('', '---------'),
    ('exact', 'Is equal to'),
    ('not_exact', 'Is not equal to'),
    ('lt', 'Lesser than'),
    ('gt', 'Greater than'),
    ('gte', 'Greater than or equal to'),
    ('lte', 'Lesser than or equal to'),
    ('startswith', 'Starts with'),
    ('endswith', 'Ends with'),
    ('contains', 'Contains'),
    ('not_contains', 'Does not contain'),
]


'''


class BannerFilter(FilterSet):
	size = CharFilter(name='size', lookup_type='icontains', distinct=True)
	class Meta:
		model = Banner
		fields = [
			'size',
			]