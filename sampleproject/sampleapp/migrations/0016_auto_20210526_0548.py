# Generated by Django 3.1.7 on 2021-05-26 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0015_auto_20210526_0543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='size',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
