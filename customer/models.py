from django_tenants.models import TenantMixin
from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
class Tenant(TenantMixin):
    name = models.CharField(max_length=100, unique=True)
    auto_create_schema = True
class Domain(DomainMixin):
    pass