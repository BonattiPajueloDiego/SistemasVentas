from crum import get_current_user
from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from app.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel


class Employee(models.Model):
    # type=models.ForeignKey(Type,on_delete=models.PROTECT)
    names = models.CharField(max_length=150, verbose_name='Nombres y Apellidos')
    dni = models.CharField(max_length=12, unique=True, verbose_name='DNI')
    phone = models.CharField(max_length=12, verbose_name='Telefono')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    # date_created=models.DateTimeField(auto_now=True,verbose_name='Fecha  y hora de creacion')
    # date_update=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de actualizacion')
    age = models.PositiveIntegerField(default=0, verbose_name='edad')
    salary = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='salario')
    state = models.BooleanField(default=True, verbose_name='estado')
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', verbose_name='imagen', null=True, blank=True)

    # cvitae=models.FileField(upload_to='cvitae/%Y/%m/%d',verbose_name='curriculum',null=True,blank=True)

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        db_table = 'empleado'
        ordering = ['id']  # de formaascendente ['/id'] <- descendentes

#===================INICIO DE BASE DE DATOS=========================
class Clients(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres ')
    Lastname = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=12, unique=True, verbose_name='DNI')
    phone = models.CharField(max_length=12, verbose_name='Telefono')
    #date_birth = models.DateField(default=datetime.now, verbose_name='Fecha de Nacimiento')
    ruc = models.CharField(max_length=11,verbose_name='Ruc',default='00000000000')
    direction = models.TextField(verbose_name='Dirección')
    description = models.TextField(verbose_name='Referencia')
    gender = models.CharField(max_length=10,choices=gender_choices,default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] ={'id':self.gender, 'name':self.get_gender_display()}
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente' # revizar
        ordering = ['id']  # de formaascendente ['/id'] <- descendentes

#pedido
class Order(models.Model):
    clients = models.ForeignKey(Clients, on_delete=models.CASCADE)
    date_order = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='SubTotal')
    igv = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='IGV')
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='TOTAL')

    def __str__(self):
        return self.clients.names

    def toJSON(self):
        item = model_to_dict(self)
        item['clients'] = self.clients.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['igv'] = format(self.igv, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_order'] = self.date_order.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.order_detail_set.all()]
        return item

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        db_table = 'pedido' #revisar
        ordering = ['id']  # de formaascendente ['/id'] <- descendentes#pedido


class Category(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre Categoria', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción Categoria')

    def __str__(self):
        return self.name

    """AQUI ES CUANDO SE REALIZA UN GUARDADO"""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user

        super(Category, self).save()

    """AQUI ES CUANDO SE REALIZA UNA eliminación

    def delete(self, using=None, keep_parents=False):
        user = get_current_user()
        if user is not None:
            self.user_delete = user
        super(Category, self).delete()"""

    # https://www.youtube.com/watch?v=-lftKKGQ0Ao&list=PLxm9hnvxnn-j5ZDOgQS63UIBxQytPdCG7&index=48

    def toJSON(self):  # aca retornamos en tipo direccionario cuando se realiza la consulta
        # item = {'id':self.id, 'name':self.name}
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'
        ordering = ['id']  # de formaascendente ['/id'] <- descendentes


class Mark(models.Model):
    name = models.CharField(max_length=150, verbose_name='nombre marca', unique=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Nombre Categoria')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción Marca')

    def __str__(self):
        return self.name

    def toJSON(self):  # aca retornamos en tipo direccionario cuando se realiza la consulta
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        db_table = 'marca'
        ordering = ['id']  # de formaascendente ['/id'] <- descendentes


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre Producto')
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', verbose_name='imagen', null=True, blank=True)
    purchase_price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio Compra')
    sale_price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio Venta')
    #stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, verbose_name='Nombre Marca')

    # cate = models.CharField(max_length=150,verbose_name='Nombre Categoria')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.avatar:
            return '{}{}'.format(MEDIA_URL, self.avatar)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['mark']=self.mark.toJSON()
        item['avatar']=self.get_image()
        item['purchase_price']=format(self.purchase_price,'.2f')
        item['sale_price']=format(self.sale_price,'.2f')

        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

        ordering = ['id']  # de formaascendente ['/id'] <- descendentes

#orden de pedido
class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0, verbose_name='Cantidad')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio ')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Subtotal')

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['order'])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'
        db_table = 'Detalle_pedido'
        ordering = ['id']  # de formaascendente ['/id'] <- descendentes"""#detalles de pedido
