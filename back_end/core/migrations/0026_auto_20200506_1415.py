# Generated by Django 2.2.10 on 2020-05-06 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_refund'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_item_select',
            field=models.ManyToManyField(blank=True, null=True, to='core.AdditionalItem'),
        ),
    ]