# Generated by Django 4.1.7 on 2023-04-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_strategyone_ce_buy_lot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategyone',
            name='repeat_order_type',
            field=models.CharField(choices=[('REPEAT', 'REPEAT'), ('NO REPEAT', 'NO REPEAT')], default='REPEAT', max_length=255),
        ),
    ]
