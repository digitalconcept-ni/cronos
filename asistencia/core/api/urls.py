from django.urls import path

from core.api.views import *

urlpatterns = [
    path('user/list/', UserListAPIView.as_view(), name='users_list'),

    # Classroom
    path('classroom/list/', ClassroomAPIView.as_view(), name='classroom_list'),
    path('classroom/create/', ClassroomCreateAPIView.as_view(), name='classroom_create'),
    path('classroom/update/<int:pk>/', ClassroomUpdateAPIView.as_view(), name='classroom_update'),
    path('classroom/delete/<int:pk>/', ClassroomDeleteAPIView.as_view(), name='classroom_delete'),
]
