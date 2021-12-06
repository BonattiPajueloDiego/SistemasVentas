# Generated by Django 3.2.8 on 2021-11-08 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_remove_mark_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='erp.category', verbose_name='Nombre Marca'),
            preserve_default=False,
        ),
    ]
