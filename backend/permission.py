from rest_framework.permissions import BasePermission
from customer.models import Tenant
from main.models import Staff

class TenantAccessPermission(BasePermission):
 

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.is_admin:
            current_tenant = getattr(request, 'tenant', None)  # Set by TenantMainMiddleware
            if not current_tenant:
                return False  # No tenant context (e.g., public schema API)
            return request.user.tenant == current_tenant

        staff_id = request.session.get('staff_id')
        if staff_id:
            try:
                staff = Staff.objects.get(id=staff_id)
                return request.method in ['GET', 'HEAD', 'OPTIONS']
            except Staff.DoesNotExist:
                return False

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if request.user.is_superuser:
            return True

        if request.user.is_admin:
            current_tenant = getattr(request, 'tenant', None)
            if not current_tenant:
                return False

            if isinstance(obj, Tenant):
                return obj == request.user.tenant
 
            return request.user.tenant == current_tenant

        staff_id = request.session.get('staff_id')
        if staff_id:
            try:
                Staff.objects.get(id=staff_id)
                return request.method in ['GET', 'HEAD', 'OPTIONS']
            except Staff.DoesNotExist:
                return False

        return False