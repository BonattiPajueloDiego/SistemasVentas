from django.urls import path
from core.erp.views.categorias.views import *
from core.erp.views.clientes.views import ClientView
from core.erp.views.marcas.views import *
from core.erp.views.order.views import OrderCreateView, OrderListView, OrderDeleteView, OrderUpdate, SaleInvoicePdfView, \
    OrderCreateView2
from core.erp.views.productos.views import *
from core.erp.views.dashboard.views import *

app_name = 'erp'
urlpatterns = [

    path('List_Category/', CategoryListView.as_view(), name='vista1'),
    path('CategoryFromView/', CategoryFromView.as_view(), name='CategoryFromView'),

    path('CategoryCreateView/', CategoryCreateView.as_view(), name='CategoryCreateView'),
    path('CategoryUpdateView/<int:pk>/', CategoryUpdateView.as_view(), name='CategoryUpdateView'),
    path('CategoryDeleteView/<int:pk>/', CategoryDeleteView.as_view(), name='CategoryDeleteView'),

    ########################################################################################

    path('MarkListView/', MarkListView.as_view(), name='MarkListView'),
    path('MarkFromView/', MarkFromView.as_view(), name='MarkFromView'),

    path('MarkCreateView/', MarkCreateView.as_view(), name='MarkCreateView'),
    path('MarkUpdateView/<int:pk>/', MarkUpdateView.as_view(), name='MarkUpdateView'),
    path('MarkDeleteView/<int:pk>/', MarkDeleteView.as_view(), name='MarkDeleteView'),

    ###########################################################################################

    path('ProductListView/', ProductListView.as_view(), name='ProductListView'),
    path('ProductCreateView/', ProductCreateView.as_view(), name='ProductCreateView'),
    path('ProductUpdateView/<int:pk>/', ProductUpdateView.as_view(), name='ProductUpdateView'),
    path('ProductDeleteView/<int:pk>/', ProductDeleteView.as_view(), name='ProductDeleteView'),

    #########################################HOME############################################

    path('dashboardView/', DashboardView.as_view(), name='DashboardView'),

    #########################################CLIENTS############################################
    path('client/', ClientView.as_view(), name='client'),



 #########################################pedidos############################################
    path('OrderCreateView/', OrderCreateView.as_view(), name='OrderCreateView'),
    path('OrderCreateView2/', OrderCreateView2.as_view(), name='OrderCreateView2'),
    path('OrderListView/', OrderListView.as_view(), name='OrderListView'),
    path('OrderDeleteView/<int:pk>/', OrderDeleteView.as_view(), name='OrderDeleteView'),
    path('OrderUpdate/<int:pk>/', OrderUpdate.as_view(), name='OrderUpdate'),
    path('SaleInvoicePdfView/<int:pk>/', SaleInvoicePdfView.as_view(), name='SaleInvoicePdfView'),



]
