from django.db import models
from django.contrib.auth.models import User
from .constants import PaymentStatus
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _


# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=250)

class Gender(models.Model):
    name = models.CharField(max_length=250)

class Product(models.Model):
    name= models.CharField(max_length=250)
    price= models.FloatField()
    image= models.ImageField(upload_to='product/')
    image1 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image2 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image3 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image4 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image5 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    description= models.TextField()
    category= models.ForeignKey(category, on_delete=models.CASCADE,null=True)
    gender= models.ForeignKey(Gender, on_delete=models.CASCADE,null=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.IntegerField()
    totalprice= models.FloatField()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=225)
    address=models.TextField()
    phone=models.CharField(max_length=12)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(_("Order ID"), max_length=40,null=True)
    payment_id = models.CharField(_("Payment ID"), max_length=36,null=True)
    signature_id = models.CharField(_("Signature ID"), max_length=128,null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.quantity})"
