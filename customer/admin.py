from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from customer.models import Domain, Tenant
from cookieapp.admin import custom_admin_site
# Register domain model
custom_admin_site.register(Domain)
# Register tenant model
custom_admin_site.register(Tenant)