from django.contrib import admin

# Register your models here.
from .models import Product,Category
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ProductResource(resources.ModelResource):
    #delete = fields.Field(widget=widgets.BooleanWidget())


    class Meta:
        model = Product


class ProductAdmin(ImportExportModelAdmin):
	search_fields = ['sku',]
	resource_class = ProductResource


class CategoryResource(resources.ModelResource):
    #delete = fields.Field(widget=widgets.BooleanWidget())


    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin):
	resource_class = CategoryResource


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)