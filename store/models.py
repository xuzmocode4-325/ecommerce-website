from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.tag


class Category(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=130, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    brand= models.CharField(max_length=250, default='unbranded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/products')
    discount = models.SmallIntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(50)])


    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
    
