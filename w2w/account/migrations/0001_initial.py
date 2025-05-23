# Generated by Django 4.2.17 on 2025-01-13 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100, verbose_name='First Name')),
                ('lastname', models.CharField(max_length=100, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=15, verbose_name='Phone')),
                ('shop_name', models.CharField(max_length=100, verbose_name='Vendor Shop Name')),
                ('shop_state', models.CharField(max_length=100, verbose_name='Vendor Shop State')),
                ('shop_city', models.CharField(max_length=100, verbose_name='Vendor Shop City')),
                ('shop_address', models.CharField(max_length=100, verbose_name='Vendor Shop Address')),
                ('password_1', models.CharField(max_length=20, verbose_name='Password')),
                ('password_2', models.CharField(max_length=20, verbose_name='Confirm Password')),
                ('user_type', models.CharField(choices=[('i_am_customer', 'Customer'), ('i_am_vendor', 'Vendor')], default='i_am_customer', max_length=20, verbose_name='User Type')),
            ],
            options={
                'verbose_name': 'Registered Users',
                'verbose_name_plural': 'Registered Users',
                'ordering': ['-id'],
            },
        ),
    ]
