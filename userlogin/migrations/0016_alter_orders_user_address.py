# Generated by Django 3.2.6 on 2021-09-17 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0015_rename_products_id_orders_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='user_address',
            field=models.CharField(max_length=2500),
        ),
    ]
