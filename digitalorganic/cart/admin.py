from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
from .models import Cart,CartItem,Order



class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
    search_fields=["customer__user__username",]    

class OrderAdmin(ImportExportModelAdmin):
	resource_class = OrderResource



class CartAdmin(admin.ModelAdmin):
	class Meta:
		model = Cart

'''
class OrderAdmin(admin.ModelAdmin):
	class Meta:
		model=Order
	search_fields=["customer__user__username",]		
'''
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order,OrderAdmin)
