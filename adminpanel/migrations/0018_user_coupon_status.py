# Generated by Django 3.2.6 on 2021-10-07 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0017_user_coupon_offer_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_coupon',
            name='status',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
