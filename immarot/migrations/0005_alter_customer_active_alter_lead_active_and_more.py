# Generated by Django 4.2.11 on 2024-12-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immarot', '0004_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='active',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3, verbose_name='Active?'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='active',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3, verbose_name='Active?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3, verbose_name='Active?'),
        ),
    ]
