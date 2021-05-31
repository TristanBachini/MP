# Generated by Django 3.1.7 on 2021-05-26 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0016_auto_20210526_0548'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sampleapp.size'),
        ),
    ]
