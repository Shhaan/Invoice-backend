from django.contrib import admin
from django.contrib.admin import AdminSite 
from .models import Account ,SocialMedia
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin as DefaultTokenAdmin
from main.models import Product

class CustomAdminSite(AdminSite):
    def has_permission(self, request):
        if request.user.is_superuser:
            return super().has_permission(request)
        return False   

custom_admin_site = CustomAdminSite(name='custom_admin')

class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'is_admin', 'is_superuser', 'is_staff', 'created_at', 'updated_at']
    search_fields = ['email']

custom_admin_site.register(Account, AccountAdmin)  


class TokenAdmin(DefaultTokenAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.key:
            obj.save()  # This auto-generates the key
        else:
            super().save_model(request, obj, form, change)

custom_admin_site.register(Token, TokenAdmin)
custom_admin_site.register(SocialMedia)
