# Generated by Django 2.2 on 2020-04-18 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_category_sub_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='sub_category',
            new_name='parent_category',
        ),
    ]
