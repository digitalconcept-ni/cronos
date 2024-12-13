from django.urls import path

from core.registration.views.career import CareerListView, CareerCreateView, CareerChangeView
from core.registration.views.classroom import ClassroomListView,ClassroomCreateView,ClassroomChangeView
from core.registration.views.departament import DepartamentListView, DepartamentCreateView, DepartamentChange
from core.registration.views.group import GroupListView, GroupCreateView, GroupChangeView
from core.registration.views.pensum import PensumListView, PensumCreateView, PensumChangeView
from core.registration.views.subject import SubjectListView, SubjectCreateView, SubjectChangeView
from core.registration.views.Inscription import InscriptionListView, InscriptionCreateView, InscriptionChangeView




urlpatterns = [
    # departament
    path('departament/', DepartamentListView.as_view(), name='departament_list'),
    path('departament/add/', DepartamentCreateView.as_view(), name='departament_add'),
    path('departament/change/<int:pk>/', DepartamentChange.as_view(), name='departament_change'),

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

    # Group
    path('group/', GroupListView.as_view(), name='group_list'),
    path('group/add/', GroupCreateView.as_view(), name='group_add'),
    path('group/change/<int:pk>/', GroupChangeView.as_view(), name='group_change'),

    # Classroom
    path('classroom/', ClassroomListView.as_view(), name='classroom_list'),
    path('classroom/add/', ClassroomCreateView.as_view(), name='classroom_add'),
    path('classroom/change/<int:pk>/', ClassroomChangeView.as_view(), name='classroom_change'),
    #Inscription
    path('Inscription/', InscriptionListView.as_view(), name='Inscription_list'),
    path('Inscription/add/',InscriptionCreateView.as_view(), name='Inscription_add'),
    path('Inscription/change/<int:pk>/', InscriptionChangeView.as_view(), name='Inscription_change'),
]
