# Generated by Django 4.2 on 2024-08-27 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storerate',
            name='total_rate',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
