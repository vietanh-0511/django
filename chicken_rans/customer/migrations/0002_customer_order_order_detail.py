# Generated by Django 3.2.5 on 2021-07-23 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('name_customer', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.product')),
            ],
            options={
                'unique_together': {('order', 'product')},
            },
        ),
    ]
