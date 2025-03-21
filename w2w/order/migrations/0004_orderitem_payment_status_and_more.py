# Generated by Django 4.2.17 on 2025-03-11 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('not paid', 'Not Paid'), ('refunded', 'Refunded')], default='not paid', max_length=10),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='payment_type',
            field=models.PositiveIntegerField(choices=[(0, '-'), (1, 'Stripe')], default='Stripe', verbose_name='Payment type'),
        ),
    ]
