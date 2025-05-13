from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    # You can customize the display and features of the Account model in the admin panel
    list_display = ['email', 'is_active', 'is_admin', 'is_superuser', 'is_staff', 'created_at', 'updated_at']
    search_fields = ['email']
    
    def get_model_perms(self, request):
        # Override to restrict access to the admin to only superusers
        if request.user.is_superuser:
            return super().get_model_perms(request)  # Return the default permissions for superuser
        return {}  # Return empty permissions, effectively hiding it from non-superusers

admin.site.register(Account, AccountAdmin)
