# Generated by Django 4.2 on 2024-08-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_productrate_total_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrate',
            name='total_rate',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]