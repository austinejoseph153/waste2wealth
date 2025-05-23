# Generated by Django 4.2.17 on 2025-03-10 05:09

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_remove_userregister_shop_address_and_more'),
        ('product', '0003_alter_wastecategory_options_cartitem_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('sub_total', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=8, verbose_name='Subtotal')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Date Of Delivery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('slug', models.SlugField(default=False, max_length=300)),
                ('status', models.PositiveIntegerField(choices=[(1, 'Active'), (2, 'Pending verification'), (3, 'Verified'), (4, 'Failed'), (5, 'Canceled')], default=1, verbose_name='Status')),
                ('currency', models.CharField(choices=[('NGN', 'NGN')], default='NGN', max_length=3)),
                ('description', models.TextField(blank=True, help_text='will only display the first 127 chars.', null=True, verbose_name='Description')),
                ('subtotal', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='Automatic if payment requests items', max_digits=8, verbose_name='Subtotal')),
                ('transaction_fee', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=5, verbose_name='Stripe transaction fee')),
                ('automatic_fee', models.BooleanField(default=False, verbose_name='Automatic calculation of the  or Stripe transaction fee')),
                ('payment_type', models.PositiveIntegerField(choices=[('', '-'), ('stripe', 'Stripe')], default='Stripe', verbose_name='Payment type')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='Payment date')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='Default Oder')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('order_description', models.TextField()),
            ],
            options={
                'verbose_name': 'shipping Address',
                'verbose_name_plural': 'Shipping Address',
            },
        ),
        migrations.CreateModel(
            name='PaymentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Amount')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.orderitem', verbose_name='product ordered')),
                ('payment_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.paymenthistory')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='Shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.shippingaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.userregister'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.vendor'),
        ),
    ]
