

from django.urls import path
from core.login.views import *

urlpatterns = [
    path('', LoginFromView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
]