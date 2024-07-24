# Generated by Django 5.0.7 on 2024-07-24 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='description')),
                ('price', models.IntegerField(verbose_name='price')),
                ('seller', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='products/%Y/%m/%d')),
                ('category', models.ManyToManyField(to='shop.category', verbose_name='Категория')),
            ],
        ),
    ]
