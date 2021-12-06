from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Order
from core.reports.forms import ReportForm

from django.db.models.functions import Coalesce
from django.db.models import Sum


class ReportOrderView(LoginRequiredMixin, ValidatePermissionRequiredMixin,TemplateView):
    template_name = 'order/report.html'
    success_url = reverse_lazy('ReportOrderView')
    permission_required = 'view_user'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        valor={}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Order.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_order__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.clients.names,
                        s.date_order.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.igv, '.2f'),
                        format(s.total, '.2f'),
                    ])

                subtotal = search.aggregate(r=Sum('subtotal')).get('r')
                igv = search.aggregate(r=Sum('igv')).get('r')
                total = search.aggregate(r=Sum('total')).get('r')

                """ HAY UN ERROR CUANDO NO HAY PEDIDOS EN EL DIA SE DEBE DE SELECCIONAR UN CAMPO
                PARA DAR SOLUCION AL PROBLE 
                DIEGO REVISA EL Coalesce por que eso te debe de redondear a  0
                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')"""

                data.append([
                    '---',
                    '---',
                    '---',
                    subtotal,
                    igv,
                    total,

                    format(subtotal, '.2f'),
                    format(igv, '.2f'),
                    format(total, '.2f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Pedidos'
        context['nombre'] = 'Reportes'
        context['list_url'] = reverse_lazy('ReportOrderView')
        context['form'] = ReportForm()
        return context
