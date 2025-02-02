# Generated by Django 4.2.11 on 2024-12-02 13:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('immarot', '0006_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('active', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3, verbose_name='Active?')),
                ('date', models.DateField(verbose_name='Date')),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='immarot.customer', verbose_name='Customer Name')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='immarot.product', verbose_name='Product')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='immarot.project', verbose_name='Project')),
                ('seller_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='immarot.seller', verbose_name='Seller Name')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
