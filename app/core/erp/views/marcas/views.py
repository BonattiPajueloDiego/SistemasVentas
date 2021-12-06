from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from django.shortcuts import render, HttpResponseRedirect

from core.erp.forms import MarcaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Mark


class MarkListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Mark
    template_name = 'marcas/List.html'
    permission_required = 'view_mark'
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Mark.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Marcas'
        context['create_url'] = reverse_lazy('erp:MarkCreateView')
        context['list_url'] = reverse_lazy('erp:MarkListView')
        context['nombre'] = 'Marcas'

        return context


class MarkCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Mark
    form_class = MarcaForm
    template_name = 'marcas/Create.html'
    success_url = reverse_lazy('erp:MarkListView')
    permission_required = 'add_mark'
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # agregar en marcas create
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No a ingresado ningun Dato'

            # data = Category.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Marcas'
        context['list_url'] = reverse_lazy('erp:MarkListView')
        context['nombre'] = 'Marcas'
        context['action'] = 'add'
        return context


class MarkUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Mark
    form_class = MarcaForm
    template_name = 'marcas/Create.html'
    success_url = reverse_lazy('erp:MarkListView')
    permission_required = 'add_client'
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No a ingresado ningun Dato'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Marcas'
        context['list_url'] = reverse_lazy('erp:MarkListView')
        context['nombre'] = 'Marcas'
        context['action'] = 'edit'
        return context


class MarkDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Mark
    template_name = 'marcas/Delete.html'
    success_url = reverse_lazy('erp:MarkListView')  # retorna una vez que la eliminacion se realiza
    permission_required = 'delete_client'
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de Marcas'
        context['list_url'] = reverse_lazy('erp:MarkListView')
        context['nombre'] = 'Marcas'
        # context['action'] = 'edit'
        return context


class MarkFromView(FormView):  # verifica si mi formulario es valido
    form_class = MarcaForm
    template_name = 'marcas/Create.html'
    success_url = reverse_lazy('erp:MarkListView')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'From | Marcas'
        context['list_url'] = reverse_lazy('erp:MarkListView')
        context['nombre'] = 'Marcas'
        context['action'] = 'add'
        return context

    # revisar n°36
