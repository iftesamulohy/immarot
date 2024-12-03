# Generated by Django 4.2.11 on 2024-12-02 13:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immarot', '0005_alter_customer_active_alter_lead_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('active', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3, verbose_name='Active?')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
