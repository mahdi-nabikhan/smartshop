# Generated by Django 4.2 on 2024-08-21 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_product_price_after'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrate',
            name='total_rate',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]