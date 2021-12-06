#from django.test import TestCase
# Create your tests here.
import random

from app.wsgi import *
from core.erp.models import Category,Mark,Product

"""trabajando con el ORM"""
"""#Listar
queryList=Category.objects.all()
print(queryList)"""

#insertar datos
"""t=Category()
t.name='BEBIDAS'
t.save()"""
"""
data = [{'GLORIA','TIPOS DELECHES'}, 'LABALLI', 'MOLITALIA', 'DON BITUTE', 'ESPIGA DE ORO',
        'AYUDIN', 'SAN CARLOS', 'SAPOLIO ', 'AZUCAR ANDAHUASY',
        'LAIBE']

for i in data:
    mar = Mark(name=i)
    mar.save()
    print('Guardado registro N°{}'.format(mar.id))
"""
#Editar
"""t=Category.objects.get(id=1)
t.name='VENDEDOR'
t.save()"""

#Eliminar


H=Category.objects.all()
H.delete()



