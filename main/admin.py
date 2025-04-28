from django.contrib import admin
from .models import Product, Category, Customize, DealoftheDay, BestSeller    
from invoice.models import Invoice,InvoiceItem 

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name','category__name')
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Customize)
admin.site.register(DealoftheDay)
admin.site.register(BestSeller)
admin.site.register(Invoice)
admin.site.register(InvoiceItem) 
 


