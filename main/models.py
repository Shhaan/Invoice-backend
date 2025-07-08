from django.db import models
from cookieapp.models import Account
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    image = models.ImageField(upload_to='categories')
    as_piece = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price =  models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quantity = models.CharField(max_length=100)
    discription  = models.TextField( null=True)
    count = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    image = models.ImageField(upload_to='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_piece = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    code = models.CharField(max_length=25,unique=True)
    take_away = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Customize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='customize')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='customize',null=True)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.product.name} - {self.name}"


class DealoftheDay(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='dealofday')
    price = models.IntegerField(default=0   )
    is_available = models.BooleanField(default=True)
    quantity = models.CharField(max_length=100 )
    def __str__(self):
        return f"{self.product.name} - deal of the day -{self.price}"
class BestSeller(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.product.name} "


class Carousel(models.Model):
    image = models.ImageField(upload_to='carousel')


class Configration(models.Model):   
    parameter_name = models.CharField(max_length=100)
    parameter_value = models.TextField()


    def __str__(self):
        return f"{self.parameter_name} - {self.parameter_value}"
     