# Generated by Django 5.1.5 on 2025-02-03 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
