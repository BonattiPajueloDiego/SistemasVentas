import json
import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse

from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView, View

from xhtml2pdf import pisa

from core.erp.forms import OrderForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Order, Product, Order_detail


class OrderListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Order
    template_name = 'order/List.html'
    success_url = reverse_lazy('erp:OrderListView')
    permission_required = 'view_order'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Order.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in Order_detail.objects.filter(order_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pedidos'
        context['create_url'] = reverse_lazy('erp:OrderCreateView')
        context['list_url'] = reverse_lazy('erp:OrderListView')
        context['nombre'] = 'Pedidos'
        return context


class OrderCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/Create.html'
    success_url = reverse_lazy('erp:OrderCreateView')
    permission_required = 'add_order'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # agregar en marcas create
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)

            elif action == 'add':
                with transaction.atomic():  # controlando posibles errores
                    vents = json.loads(request.POST['vents'])

                    order = Order()
                    order.clients_id = vents['clients']
                    order.date_order = vents['date_order']
                    order.subtotal = float(vents['subtotal'])
                    order.igv = float(vents['igv'])
                    order.total = float(vents['total'])

                    order.save()

                    for i in vents['products']:
                        det = Order_detail()
                        det.order_id = order.id
                        det.product_id = i['id']
                        det.cantidad = int(i['cant'])
                        det.price = float(i['sale_price'])
                        det.subtotal = float(i['subtotal'])

                        det.save()
                    data = {'id': order.id}

            else:
                data['error'] = 'No a ingresado ningun Dato'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Pedidos'
        context['list_url'] = reverse_lazy('erp:OrderListView')
        context['nombre'] = 'Pedidos'
        context['action'] = 'add'
        context['det'] = []
        return context


class OrderCreateView2(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/Create.html'
    success_url = reverse_lazy('erp:OrderCreateView')
    permission_required = 'add_order'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # agregar en marcas create
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)

            elif action == 'add':
                with transaction.atomic():  # controlando posibles errores
                    vents = json.loads(request.POST['vents'])

                    order = Order()
                    order.clients_id = vents['clients']
                    order.date_order = vents['date_order']
                    order.subtotal = float(vents['subtotal'])
                    order.igv = float(vents['igv'])
                    order.total = float(vents['total'])

                    order.save()

                    for i in vents['products']:
                        det = Order_detail()
                        det.order_id = order.id
                        det.product_id = i['id']
                        det.cantidad = int(i['cant'])
                        det.price = float(i['sale_price'])
                        det.subtotal = float(i['subtotal'])

                        det.save()
                    data = {'id': order.id}

            else:
                data['error'] = 'No a ingresado ningun Dato'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Pedidos'
        context['list_url'] = reverse_lazy('erp:OrderCreateView')
        context['nombre'] = 'Pedidos'
        context['action'] = 'add'
        context['det'] = []
        return context


class OrderUpdate(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/Create.html'
    success_url = reverse_lazy('erp:OrderListView')
    permission_required = 'change_order'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # agregar en marcas create
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)

            elif action == 'edit':
                with transaction.atomic():  # controlando posibles errores
                    vents = json.loads(request.POST['vents'])

                    # order = Order.objects.get(pk=self.get_object().id)
                    order = self.get_object()
                    order.clients_id = vents['clients']
                    order.date_order = vents['date_order']
                    order.subtotal = float(vents['subtotal'])
                    order.igv = float(vents['igv'])
                    order.total = float(vents['total'])
                    order.save()

                    order.order_detail_set.all().delete()

                    for i in vents['products']:
                        det = Order_detail()
                        det.order_id = order.id
                        det.product_id = i['id']
                        det.cantidad = int(i['cant'])
                        det.price = float(i['sale_price'])
                        det.subtotal = float(i['subtotal'])

                        det.save()
                    data = {'id': order.id}

            else:
                data['error'] = 'No a ingresado ningun Dato'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in Order_detail.objects.filter(order_id=self.get_object().id):
                item = i.product.toJSON()
                item['cant'] = i.cantidad
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Pedido'
        context['list_url'] = reverse_lazy('erp:OrderListView')
        context['nombre'] = 'Pedidos'
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        return context


class OrderDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Order
    template_name = 'order/Delete.html'
    success_url = reverse_lazy('erp:OrderListView')
    permission_required = 'delete_order'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Pedido'
        context['nombre'] = 'Pedidos'
        context['list_url'] = reverse_lazy('erp:OrderListView')
        return context


class SaleInvoicePdfView(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('order/invoce.html')
            context = {
                'order': Order.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'INVERSIONES CHA & BI S.R.L.', 'ruc': '20602840001',
                         'address': 'MAYORAZGO 1 LIMA, LIMA - SAN MARTIN DE PORRES'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:OrderListView'))
