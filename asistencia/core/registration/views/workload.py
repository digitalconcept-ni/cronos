import json

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm, CareerForm, UserSubjectForm
from core.registration.models import Departament, Career, UserSubject, Subject
from core.user.mixins import ValidatePermissionRequiredMixin
from core.user.models import User
from core.utilities import validate_delete

entity = 'Carga horaria'
title = 'Asignaturas asignadas'

class WorkloadListView(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'workload/list.html'
    permission_required = 'view_usuario_asignatura'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [s.toListSubject() for s in User.objects.select_related().filter(roll='TEACHER')]


            elif action == 'delete':
                # Validamos si el usuario cuenta con el permiso de eliminar el registor
                if validate_delete(self.permission_required):
                    cli = UserSubject.objects.get(id=request.POST['id'])
                    cli.delete()
                else:
                    data['error'] = 'No tiene permiso para realizar la siguiente acción'

            else:
                data['error'] = 'Ha ocurrido un error con el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['entity'] = entity
        context['create_url'] = reverse_lazy('workload_add')
        context['list_url'] = reverse_lazy('workload_list')

        return context

class WorkloadAddView(ValidatePermissionRequiredMixin, CreateView):
    model = UserSubject
    form_class = UserSubjectForm
    template_name = 'workload/create.html'
    success_url = reverse_lazy('workload_list')
    url_redirect = success_url
    permission_required = 'add_subject'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_subject':
                data = []
                term = request.POST['term'].strip()
                subject = Subject.objects.all()
                if len(term):
                    subject = subject.filter(name__icontains=term)
                for i in subject[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)

            if action == 'add':
                subjects = json.loads(request.POST['subjects'])
                print(request.POST)

                for i in subjects:
                    us = UserSubject()
                    us.user_id = request.POST['user']
                    us.subject_id = int(i['id_subject'])
                    us.save()
                data = request.user.id

                # form = self.get_form()
                # data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['entity'] = entity
        context['list_url'] = reverse_lazy('workload_list')
        context['action'] = 'add'
        return context


class CareerChangeView(ValidatePermissionRequiredMixin, UpdateView):
    model = Career
    form_class = CareerForm
    template_name = 'career/create.html'
    success_url = reverse_lazy('career_list')
    url_redirect = success_url
    permission_required = 'change_departamento'

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

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar carrera'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context