# Generated by Django 3.1.7 on 2021-06-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0026_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shoppingcart',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
