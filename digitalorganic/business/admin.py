from django.contrib import admin
from .models import Banner,Enquiry,ContactQuery,EnquiryItem
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.


class BannerResource(resources.ModelResource):
    class Meta:
        model = Banner


class BannerAdmin(ImportExportModelAdmin):
	resource_class = BannerResource


class EnquiryAdmin(admin.ModelAdmin):
	class Meta:
		model = Enquiry
	search_fields = ['info_request','mobile','pincode','first_name','last_name']	

class OrderEnquiryAdmin(admin.ModelAdmin):
	class Meta:
		model = ContactQuery
	search_fields = ['mobile','pincode','first_name','last_name']	



admin.site.register(Banner,BannerAdmin)
admin.site.register(Enquiry,EnquiryAdmin)
admin.site.register(ContactQuery,OrderEnquiryAdmin)
admin.site.register(EnquiryItem)

