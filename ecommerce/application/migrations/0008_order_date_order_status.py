# Generated by Django 4.2.5 on 2023-10-17 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_remove_orderdetail_cart_orderdetail_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(default='2023-10-10', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='', max_length=100),
        ),
    ]