# Generated by Django 4.2.11 on 2024-09-08 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_users_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
