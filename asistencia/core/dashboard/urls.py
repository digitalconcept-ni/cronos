from django.urls import path

from core.dashboard.views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    # path('ping', ping, name='ping'),
]

