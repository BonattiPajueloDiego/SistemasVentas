# Generated by Django 3.2.8 on 2021-11-08 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_mark_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='category',
        ),
    ]
