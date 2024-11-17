from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', LoginFormview.as_view(), name='login'),
    path('logout/', LogoutFormview.as_view(), name='logout'),
]
