from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from backend.permission import TenantAccessSuperUserPermission
from utils import get_response,CustomPageNumberPagination


class TenentsUserMainView(APIView):
    permission_classes = [TenantAccessSuperUserPermission]
    def post(self, request):
        serializer = TenentUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = TenentDisplaySerializer(serializer.instance).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        tenant_id = request.GET.get("id")

        if tenant_id:
            try:
                tenant = Tenant.objects.get(id=tenant_id)
                serializer = TenentDisplaySerializer(tenant)
                return get_response(False, serializer.data, status.HTTP_200_OK)
            except Tenant.DoesNotExist:
                return get_response(True, {"error": "Tenant not found."}, status.HTTP_404_NOT_FOUND)

        # If no ID is passed, return paginated list
        tenants = Tenant.objects.all()
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(tenants, request)

        if page is not None:
            serializer = TenentDisplaySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Non-paginated response
        serializer = TenentDisplaySerializer(tenants, many=True)
        return get_response(False, serializer.data, status.HTTP_200_OK)


    def put(self, request):
        tenant_id = request.data.get("id")
        if not tenant_id:
            return Response({"error": "Tenant ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TenentUpdateSerializer(tenant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":TenentDisplaySerializer(serializer.instance).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        tenant_id = request.data.get("id")
        if not tenant_id:
            return Response({"error": "Tenant ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            account = Account.objects.get(tenent=tenant)
            domain = Domain.objects.get(tenant=tenant) 
            if account.is_superuser:
                return Response({"error": "Cannot delete superuser account"}, status=status.HTTP_400_BAD_REQUEST)
            account.delete()
            domain.delete()
            tenant.delete()
            return Response({"success": "Tenant,Account,Domain has deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        