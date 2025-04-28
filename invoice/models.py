from django.db import models
from main.models import Customize,Product
# Create your models here.


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=60 )
     
    time_slot = models.CharField(max_length=70)
    is_delivery = models.BooleanField(default=False)
    building = models.CharField(max_length=70,null=True)
    Street = models.CharField(max_length=70,null=True)
    Zone = models.CharField(max_length=70,null=True)
    location = models.CharField(max_length=70,null=True)
 

    def calculate_total(self):
        total = sum(item.sub_total for item in self.items.all())
        return total
    
    def __str__(self):
        return f"Invoice #{self.id} "


 

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    productcustomize = models.ForeignKey(Product,related_name='items', on_delete=models.SET_NULL,null=True)
    product_name = models.CharField(max_length=70)
    customize = models.CharField(max_length=70)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
      
        self.sub_total = self.price * self.count   
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#000{self.invoice.pk}    - {self.count} x {self.price}"