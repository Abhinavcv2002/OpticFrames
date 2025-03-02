from django.db import models

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=250)

class Product(models.Model):
    name= models.CharField(max_length=250)
    price= models.FloatField()
    image= models.ImageField(upload_to='product/')
    description= models.TextField()
    category= models.ForeignKey(category, on_delete=models.CASCADE,null=True)

class Cart(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.IntegerField()
    totalprice= models.FloatField()


class Order(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.IntegerField()
    totalprice= models.FloatField()
    address= models.TextField()
    phone= models.CharField(max_length=250)
    status= models.CharField(max_length=250)
    date= models.DateTimeField(auto_now_add=True)