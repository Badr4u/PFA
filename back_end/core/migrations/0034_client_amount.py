# Generated by Django 2.2.10 on 2020-05-29 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_orderproduct_additional_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='amount',
            field=models.FloatField(default=300),
        ),
    ]
