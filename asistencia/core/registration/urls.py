from django.urls import path

from core.registration.views.career import CareerListView, CareerCreateView, CareerChangeView
from core.registration.views.departament import *
from core.registration.views.pensum import PensumListView, PensumCreateView, PensumChangeView
from core.registration.views.subject import SubjectListView, SubjectCreateView, SubjectChangeView

urlpatterns = [
    # departament
    path('departament/', DepartamentListView.as_view(), name='departament_list'),
    path('departament/add/', DepartamentCreateView.as_view(), name='departament_add'),
    path('departament/change/<int:pk>/', DepartamentChange.as_view(), name='departament_chenge'),

    # Career
    path('career/', CareerListView.as_view(), name='career_list'),
    path('career/add/', CareerCreateView.as_view(), name='career_add'),
    path('career/change/<int:pk>/', CareerChangeView.as_view(), name='career_change'),

    # Pensum
    path('pensum/', PensumListView.as_view(), name='pensum_list'),
    path('pensum/add/', PensumCreateView.as_view(), name='pensum_add'),
    path('pensum/change/<int:pk>/', PensumChangeView.as_view(), name='pensum_change'),


    path('subject/', SubjectListView.as_view(), name='subject_list'),
    path('subject/add/', SubjectCreateView.as_view(), name='subject_add'),
    path('subject/change/<int:pk>/', SubjectChangeView.as_view(), name='subject_change'),

]
