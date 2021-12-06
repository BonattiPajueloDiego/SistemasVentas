from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.forms import ClientForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Clients


class ClientView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    model = Clients
    template_name = 'clientes/List.html'
    permission_required = 'view_clients'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Clients.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                cli = Clients()
                cli.names = request.POST['names']
                cli.Lastname = request.POST['Lastname']
                cli.dni = request.POST['dni']
                cli.phone = request.POST['phone']
                cli.ruc = request.POST['ruc']
                # cli.date_birth = request.POST['date_birth']
                cli.direction = request.POST['direction']
                cli.description = request.POST['description']
                cli.gender = request.POST['gender']
                cli.save()
            elif action == 'edit':
                cli = Clients.objects.get(pk=request.POST['id'])
                cli.names = request.POST['names']
                cli.Lastname = request.POST['Lastname']
                cli.dni = request.POST['dni']
                cli.phone = request.POST['phone']
                cli.ruc = request.POST['ruc']
                # cli.date_birth = request.POST['date_birth']
                cli.direction = request.POST['direction']
                cli.description = request.POST['description']
                cli.gender = request.POST['gender']
                cli.save()
            elif action == 'delete':
                cli = Clients.objects.get(pk=request.POST['id'])
                cli.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('erp:client')
        context['nombre'] = 'Clientes'
        context['form'] = ClientForm()
        return context


