from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=500,default="")
    price = models.IntegerField(default=0)
    date = models.DateField(max_length=300)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product_name

class ImageGallery(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/')
    
    def __str__(self): 
        return self.product.product_name

class Cart(models.Model):
    user = models.ForeignKey(User, default=None,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_cost(self):
        return self.quantity * self.product.price