# Generated by Django 5.1.3 on 2025-01-16 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_alter_category_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="disount_percentage",
            field=models.SmallIntegerField(default=0),
        ),
    ]
