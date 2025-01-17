from django.db import models


# Create your models here.

class Coupon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.discount * 100}%"
    