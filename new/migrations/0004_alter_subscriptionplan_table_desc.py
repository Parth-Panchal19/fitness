# Generated by Django 5.0.3 on 2024-04-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0003_subscriptionplan_table_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan_table',
            name='desc',
            field=models.CharField(max_length=300),
        ),
    ]
