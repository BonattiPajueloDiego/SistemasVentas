from django.forms import *

from core.erp.models import *


class CategoriaForm(ModelForm):

    def __init__(self, *args, **kwargs):  # iniciara cargando los atributos necesarios para cada campo
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = 'off'

    class Meta:
        model = Category
        fields = '__all__'
        labels = {

        }
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una Descripción',
                    'rows': 3,
                    'cols': 3
                }
            )

        }

        exclude = ['user_update', 'user_creation', 'user_delete']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return data

    def clean(self):
        cleand = super().clean()


class MarcaForm(ModelForm):

    def __init__(self, *args, **kwargs):  # iniciara cargando los atributos necesarios para cada campo
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = 'off'

    class Meta:
        model = Mark
        fields = '__all__'
        labels = {

        }
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una Descripción',
                    'rows': 3,
                    'cols': 3
                }  # camio realizado
            )

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Clients
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'Lastname': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'phone': TextInput(
                attrs={
                    'placeholder': 'Ingrese Numero de Telefono',
                }
            ),
            'ruc': TextInput(

            ),
            'direction': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'description': TextInput(
                attrs={

                }
            ),
            'gender': Select()
        }

        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'clients': Select(attrs={
                'class': 'form-control select2',
                'style': 'width:100%'
            }
            ),
            'date_order': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_order',
                    'data-target': '#date_order',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'igv': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }
        exclude = ['user_updated', 'user_creation']
