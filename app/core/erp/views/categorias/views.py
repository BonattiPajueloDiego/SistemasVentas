from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from django.shortcuts import render, HttpResponseRedirect

from core.erp.forms import CategoriaForm
from core.erp.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from core.erp.models import Category


def caterodryList(request):
    data = {
        'title': 'Listado de Categoria',
        'Category': Category.object.all()
    }
    return render(request, 'categorias/List.html', data)


class CategoryListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):#IsSuperuserMixin

    model = Category
    template_name = 'categorias/List.html'
    permission_required = 'view_category'

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorias'
        context['create_url'] = reverse_lazy('erp:CategoryCreateView')
        context['list_url'] = reverse_lazy('erp:vista1')
        context['nombre'] = 'Categorias'
        return context


class CategoryCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoriaForm
    template_name = 'categorias/Create.html'
    success_url = reverse_lazy('erp:vista1')
    permission_required = 'add_category'
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
        context['title'] = 'Creación de Categorias'
        context['list_url'] = reverse_lazy('erp:vista1')
        context['nombre'] = 'Categorias'
        context['action'] = 'add'
        return context


class CategoryUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoriaForm
    template_name = 'categorias/Create.html'
    success_url = reverse_lazy('erp:vista1')
    permission_required = 'change_category'
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
        context['title'] = 'Edición de Categorias'
        context['list_url'] = reverse_lazy('erp:vista1')
        context['nombre'] = 'Categorias'
        context['action'] = 'edit'
        return context


class CategoryDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'categorias/Delete.html'
    success_url = reverse_lazy('erp:vista1')  # retorna una vez que la eliminacion se realiza

    permission_required = 'delete_category'
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
        context['title'] = 'Eliminación de Categorias'
        context['list_url'] = reverse_lazy('erp:vista1')
        context['nombre'] = 'Categorias'
        # context['action'] = 'edit'
        return context


class CategoryFromView(FormView):  # verifica si mi formulario es valido
    form_class = CategoriaForm
    template_name = 'categorias/Create.html'
    success_url = reverse_lazy('erp:vista1')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'From | Categorias'
        context['list_url'] = reverse_lazy('erp:vista1')
        context['nombre'] = 'Categorias'
        context['action'] = 'add'
        return context

    # revisar n°36
