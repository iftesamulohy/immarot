# Generated by Django 4.2.11 on 2024-09-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_specialcta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialcta',
            name='button_text',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='specialcta',
            name='button_url',
            field=models.URLField(default=None),
        ),
        migrations.AlterField(
            model_name='specialcta',
            name='icon',
            field=models.ImageField(default=None, upload_to='icons/'),
        ),
        migrations.AlterField(
            model_name='specialcta',
            name='title',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
