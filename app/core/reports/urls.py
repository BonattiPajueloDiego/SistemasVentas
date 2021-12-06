from django.urls import path

from core.reports.views import *

urlpatterns = [
    path('ReportOrderView/', ReportOrderView.as_view(), name='ReportOrderView'),
]
