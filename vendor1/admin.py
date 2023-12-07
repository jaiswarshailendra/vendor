from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Vendor_Model)
admin.site.register(Purchase_Order_Model)
admin.site.register(Historical_Performance_Model)