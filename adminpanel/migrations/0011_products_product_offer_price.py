# Generated by Django 3.2.6 on 2021-10-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0010_auto_20211001_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_offer_price',
            field=models.IntegerField(null=True),
        ),
    ]
