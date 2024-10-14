from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=130, unique=True)

    class Meta:
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.names


class Product(models.Model):
    title = models.CharField(max_length=250)
    brand= models.CharField(max_length=250, default='unbranded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/products')

    class Meta:
        verbose_name_plural = 'products'


    def __str__(self):
        return self.title
    
