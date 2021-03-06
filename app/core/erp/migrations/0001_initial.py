# Generated by Django 3.2.8 on 2021-11-07 22:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre Categoria')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción Categoria')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categoria',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=150, verbose_name='Nombres ')),
                ('Lastname', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('dni', models.CharField(max_length=12, unique=True, verbose_name='DNI')),
                ('phone', models.CharField(max_length=12, verbose_name='Telefono')),
                ('date_birth', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Nacimiento')),
                ('derection', models.TextField(verbose_name='Dirección')),
                ('sex', models.CharField(max_length=10, verbose_name='SEXO')),
                ('descrption', models.TextField(verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'cliente',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=150, verbose_name='Nombres y Apellidos')),
                ('dni', models.CharField(max_length=12, unique=True, verbose_name='DNI')),
                ('phone', models.CharField(max_length=12, verbose_name='Telefono')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Registro')),
                ('age', models.PositiveIntegerField(default=0, verbose_name='edad')),
                ('salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='salario')),
                ('state', models.BooleanField(default=True, verbose_name='estado')),
                (
                'avatar', models.ImageField(blank=True, null=True, upload_to='avatar/%Y/%m/%d', verbose_name='imagen')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'db_table': 'empleado',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='nombre marca')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción Marca')),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
                'db_table': 'marca',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_order', models.DateTimeField(auto_now=True, verbose_name='Fecha  y hora de pedido')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='SubTotal')),
                ('igv', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='IGV')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='TOTAL')),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.clients')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.employee')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'pedido',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre Producto')),
                (
                'avatar', models.ImageField(blank=True, null=True, upload_to='avatar/%Y/%m/%d', verbose_name='imagen')),
                ('purchase_price',
                 models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio Compra')),
                ('sale_price',
                 models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio Venta')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=0, verbose_name='Cantidad')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio ')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Subtotal')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.product')),
            ],
            options={
                'verbose_name': 'Detalle',
                'verbose_name_plural': 'Detalles',
                'db_table': 'Detalle_pedido',
                'ordering': ['id'],
            },
        ),
    ]
