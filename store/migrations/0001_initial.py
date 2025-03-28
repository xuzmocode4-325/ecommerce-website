# Generated by Django 5.1.2 on 2024-11-05 03:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=128)),
                ("slug", models.SlugField(max_length=130, unique=True)),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag", models.TextField(max_length=128)),
                ("slug", models.SlugField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                ("brand", models.CharField(default="unbranded", max_length=250)),
                ("description", models.TextField(blank=True)),
                ("slug", models.SlugField(max_length=150, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=4)),
                ("image", models.ImageField(upload_to="images/products")),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product",
                        to="store.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "products",
            },
        ),
    ]
