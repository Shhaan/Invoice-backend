from rest_framework import serializers,exceptions
from .models import Category,DealoftheDay,Customize,Product,BestSeller
from django.utils.datastructures import MultiValueDict


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True,required=False)
    class Meta:
        model = Category
        fields = ["id","name","image","as_piece",'is_available'] 
 

class DealoftheDaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    image = serializers.ImageField(source='product.image')
    original_price = serializers.CharField(source='product.price')
    product_id = serializers.IntegerField(source='product.id')
    take_away = serializers.IntegerField(source='product.take_away')
    code = serializers.CharField(source='product.code')
    class Meta:
        model = DealoftheDay
        fields = ["id","name","image","original_price","quantity",'price','product_id','take_away','code'] 

class ProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id')

    class Meta:
        model = Product
        exclude = ['updated_at', 'created_at', 'id']

class CustomizeSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    customization_id = serializers.IntegerField(source='id')
    class Meta:
        model = Customize
        fields = ["name","image","product","customization_id"] 
    def get_product(self,obj):
        
        return ProductSerializer(obj.product).data

class BestSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BestSeller
        fields = []   

    def to_representation(self, instance):
        product_data = ProductSerializer(instance.product).data
        deal = DealoftheDay.objects.filter(product=instance.product).first()
        if deal:
            product_data['original_price'] = product_data['price']
            product_data['price'] = deal.price
        return product_data

 

class ProductMainSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source = 'id')
    category = serializers.CharField(source = "category.name")
    class Meta:
        model = Product
        exclude = ['updated_at', 'created_at', 'id']

    def to_representation(self, instance):
        product_data = super().to_representation(instance)
        deal = DealoftheDay.objects.filter(product=instance).first()
        if deal:
            product_data['original_price'] = product_data['price']
            product_data['price'] = deal.price
        return product_data
 
class ProductUploadSerializer(serializers.ModelSerializer):
    customize = serializers.ListField(write_only=True,required=False)   
    is_bestseller = serializers.BooleanField(write_only=True,required=False)   
    image = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
 
        is_bestseller = validated_data.pop('is_bestseller', False)
        customize_data = validated_data.pop('customize', [])

        product = super().create(validated_data)

        if is_bestseller:
            BestSeller.objects.create(product=product)

        if customize_data:
            try:
                for item in customize_data:
                    if isinstance(item, MultiValueDict):
                        text_value = item.get('[text]', [None])
                        image_value = item.get('[image]')
                        if isinstance(image_value, list):
                            image_value = image_value[0]   
                    else:
                        text_value = item.get('text')
                        image_value = item.get('image')[0] if 'image' in item and isinstance(item['image'], list) else item.get('image')

    

                    if text_value:
                        Customize.objects.create(
                            product=product,
                            name=text_value,
                            image=image_value
                        )
            except Exception as e:
                raise exceptions.ValidationError({'error':True,'message':str(e)})
        return product
    def update(self, instance, validated_data):
        is_bestseller = validated_data.pop('is_bestseller', None)
        customize_data = validated_data.pop('customize', [])

        product =instance

        if is_bestseller == True and not BestSeller.objects.filter(product=product).exists():
            BestSeller.objects.create(product=product)
        elif is_bestseller ==False:
            BestSeller.objects.filter(product=product).delete()
        if customize_data:
            Customize.objects.filter(product=product).delete()
            try:
                for item in customize_data:
                    if isinstance(item, MultiValueDict):
                        text_value = item.get('[text]', [None])
                        image_value = item.get('[image]')
                        if isinstance(image_value, list):
                            image_value = image_value[0]   
                    else:
                        text_value = item.get('text')
                        image_value = item.get('image')[0] if 'image' in item and isinstance(item['image'], list) else item.get('image')

    

                    if text_value:
                        Customize.objects.create(
                            product=product,
                            name=text_value,
                            image=image_value
                        )
            except Exception as e:
                raise exceptions.ValidationError({'error':True,'message':str(e)})
        else:
            Customize.objects.filter(product=product).delete()

        return super().update(instance, validated_data)
     

class DealoftheDayuploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealoftheDay
        fields = '__all__'

    def validate(self, attrs):
        product = attrs.get('product')
        price = attrs.get('price')

        if product and price > product.price:
            raise exceptions.ValidationError({'error': True, 'message': 'The price must be less than the product price'})
        
        if not  product.is_available:
            raise exceptions.ValidationError({'error': True, 'message': 'The product is not available in stock'})

        return attrs

    def create(self, validated_data):
        product = validated_data.get('product')
        
        if product and DealoftheDay.objects.filter(product=product).exists():
            raise exceptions.ValidationError({'error': True, 'message': 'Deal of the day with this product already exists'})
        
        if not product:
            raise exceptions.ValidationError({'error': True, 'message': 'Product is required'})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        product = validated_data.get('product', instance.product)
        
        if DealoftheDay.objects.filter(product=product).exclude(id=instance.id).exists():
            raise exceptions.ValidationError({'error': True, 'message': 'Deal of the day with this product already exists'})
        
        return super().update(instance, validated_data)

class CustomizeproducteditSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source = 'name')
    class Meta:
        model = Customize
        fields = ["text","image","id"]  
    
class ProducteditgetSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id')
    category = serializers.CharField(source='category.name')
    customize = serializers.SerializerMethodField()
    is_bestseller = serializers.SerializerMethodField()
 
    class Meta:
        model = Product
        exclude = ['updated_at', 'created_at', 'id']

    def get_customize(self, obj):
        query = Customize.objects.filter(product = obj)
        return CustomizeproducteditSerializer(query,many=True).data  

    def get_is_bestseller(self, obj):
        query = BestSeller.objects.filter(product=obj)
        if query.exists():
            return True
        else:
            return False
        



class ProductInvoicegetSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id')
    category = serializers.CharField(source='category.name')
    customize = serializers.SerializerMethodField()
    is_bestseller = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        exclude = ['updated_at', 'created_at', 'id']

    def get_customize(self, obj):
        query = Customize.objects.filter(product = obj)
        return CustomizeproducteditSerializer(query,many=True).data  
    def get_price(self,obj):
        deal = DealoftheDay.objects.filter(product=obj).first()

        return obj.price if not deal else deal.price

    def get_is_bestseller(self, obj):
        query = BestSeller.objects.filter(product=obj)
        if query.exists():
            return True
        else:
            return False