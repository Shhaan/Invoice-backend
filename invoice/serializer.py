from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Invoice,InvoiceItem
from main.serializers import CustomizeproducteditSerializer
from main.models import *


 
 
class InvoiceItemSerializer(serializers.ModelSerializer):
    
     
    class Meta:
        model = InvoiceItem
        fields = "__all__" 
 
  
 
class Invoiceserializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    product  = serializers.ListSerializer(child = serializers.JSONField(),write_only=True,required =False)   
    class Meta:
        model = Invoice
        exclude = ['created_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('product', [])
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
             
            product_id = item_data.get('product')
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError({
                    'error': True,
                    'message': f"Product with id {product_id} does not exist."
                })

            InvoiceItem.objects.create(
                    invoice=invoice,
                    productcustomize=product,
                    product_name=product.name + ' ' +f"{item_data.get('customize','')}",
                    customize = item_data.get('customize',''),
                    price=item_data.get('price'),
                    count=item_data.get('count'),
                    sub_total=item_data.get('price') * item_data.get('count')
                    
                )

        return invoice
    def update(self, instance,validated_data):
        
        items_data = validated_data.pop('product', [])
        invoice =Invoice.objects.filter(id= instance.pk).update(**validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for item_data in items_data:
                
                product_id = item_data.get('product')
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    raise ValidationError({
                        'error': True,
                        'message': f"Product with id {product_id} does not exist."
                    })

                InvoiceItem.objects.create(
                        invoice=instance,
                        productcustomize=product,
                        product_name=product.name + ' ' +f"{item_data.get('customize','')}",
                        customize = item_data.get('customize',''),
                        price=item_data.get('price'),
                        count=item_data.get('count'),
                        sub_total=item_data.get('price') * item_data.get('count')
                        
                    )
            

        return instance

    
    def get_items(self, instance):
        items = InvoiceItem.objects.filter(invoice=instance)
        data = []
        
        for item in items:
             
            
            name = item.productcustomize.name if item.productcustomize else None
            count = item.productcustomize.count if item.productcustomize else None

            image = item.productcustomize.image.url if item.productcustomize and item.productcustomize.image and item.productcustomize.image.name else None
             
            
            data.append( {
                    'product_id': item.productcustomize.id if item.productcustomize else None,
                    'name':name,
                    'image':image,
                    'price': item.price ,
                    'count': item.count, 
                    'actualcount':count,
                    'sub_total': item.sub_total,
                    'customize':item.customize,
                    'id':item.pk,
                })

           
        return data
    def get_total(self,instance):
        return instance.calculate_total()
    

class Invoicepdfserializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        exclude = ['created_at']
    
    def get_total(self,instance):
        return instance.calculate_total()
    def get_items(self,instance):
        inocieitem = InvoiceItem.objects.filter(invoice = instance)
        return InvoiceItemSerializer(inocieitem,many=True).data

        