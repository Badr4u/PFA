# Generated by Django 2.2 on 2020-04-19 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_product_badge_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='No description available for this product'),
        ),
    ]
