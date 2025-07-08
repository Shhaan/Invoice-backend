from rest_framework import serializers
from .models import Tenant,Domain
from cookieapp.models import Account,SocialMedia
from django.conf import settings

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        exclude = ['id']

class TenentUploadSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    domain = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    logo = serializers.FileField(required=True)
    company_name = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        domain_name = attrs.get('domain')
        company_name = attrs.get('company_name')
        schema_name = company_name.lower().replace(' ', '-')  # consistent normalization

        attrs['schema_name'] = schema_name

        if Tenant.objects.filter(name=attrs['name']).exists():
            raise serializers.ValidationError({'name': 'Tenant with this name already exists.'})
        if Tenant.objects.filter(schema_name=schema_name).exists():
            raise serializers.ValidationError({'company_name': 'Tenant with this company name already exists.'})
        if Domain.objects.filter(domain=domain_name).exists():
            raise serializers.ValidationError({'domain': 'Domain already exists.'})
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'User with this email already exists.'})
        if Account.objects.filter(company_name=company_name).exists():
            raise serializers.ValidationError({'company_name': 'User with this company name already exists.'})

        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        domain_name = validated_data.pop('domain')
        logo = validated_data.pop('logo')
        company_name = validated_data.pop('company_name') 

        tenant = Tenant.objects.create(**validated_data)
        
        domain_name = domain_name.lower()  
        Domain.objects.create(domain=domain_name, tenant=tenant, is_primary=True)

        account = Account.objects.create(
            email=email,
            is_admin=True,
            is_active=True,
            is_staff=True,
            company_name=company_name,
            company_logo=logo,
            tenent=tenant
        )
        account.set_password(password)
        account.save()

        return tenant
    
class TenentDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        exclude = ['id']
    def to_representation(self, instance):
        user = None
        domain = None
        try:
            user = Account.objects.get(tenent=instance)
        except Account.DoesNotExist:
            pass
        try:
            domain = Domain.objects.get(tenant=instance)
        except Domain.DoesNotExist:
            pass
        domain_url = settings.DOMAIN.format(domain=domain.domain) if domain else None
        try:
            social = SocialMedia.objects.filter(user=user)
        except:
            pass
        return {
            'id': instance.id,
            'name': instance.name,
            'is_admin': user.is_admin if user else None,
            "is_superuser":user.is_superuser if user else None,
            'schema_name': instance.schema_name,
            'logo': user.company_logo.url if user and user.company_logo else None,
            'company_name': user.company_name if user else None,
            'address': user.address if user else None,
            'phone': user.phone if user else None,
            'country_code': user.country_code if user else None,
            'domain':domain_url,
            'email': user.email if user else None,
            'social':SocialMediaSerializer(social,many=True).data if social.exists() else []

        }
    
class TenentUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    domain = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    logo = serializers.FileField(required=False)
    company_name = serializers.CharField(required=False)

    def validate(self, attrs): 
        tenant = self.instance
        try:
            account = tenant.account  # Fix here
        except Account.DoesNotExist:
            raise serializers.ValidationError({"account": "Associated account does not exist."})
        new_name = attrs.get('name') 
        new_domain = attrs.get('domain')
        new_email = attrs.get('email')
        new_company_name = attrs.get('company_name')

        if new_name and new_name != tenant.name:
            if Tenant.objects.filter(name=new_name).exclude(id=tenant.id).exists():
                raise serializers.ValidationError({'name': 'Tenant with this name already exists.'})

        
        if new_domain:
            domain_qs = Domain.objects.filter(domain=new_domain).exclude(tenant=tenant)
            if domain_qs.exists():
                raise serializers.ValidationError({'domain': 'Domain already exists.'})

        if new_email and new_email != account.email:
            if Account.objects.filter(email=new_email).exclude(id=account.id).exists():
                raise serializers.ValidationError({'email': 'User with this email already exists.'})

        if new_company_name and new_company_name != account.company_name:
            if Account.objects.filter(company_name=new_company_name).exclude(id=account.id).exists():
                raise serializers.ValidationError({'company_name': 'User with this company name already exists.'})

        return attrs

    def update(self, instance, validated_data):
        # Tenant update
        instance.name = validated_data.get('name', instance.name) 
        instance.save()

        # Domain update
        domain_name = validated_data.get('domain')
        if domain_name:
            domain_name = domain_name.lower() 
            domain = Domain.objects.filter(tenant=instance).first()
            if domain:
                domain.domain = domain_name
                domain.save()

        # Account update
        account = instance.account
        if account:
            account.email = validated_data.get('email', account.email)
            account.company_name = validated_data.get('company_name', account.company_name)
            if 'logo' in validated_data:
                account.company_logo = validated_data['logo'] 
            account.save()

        return instance
