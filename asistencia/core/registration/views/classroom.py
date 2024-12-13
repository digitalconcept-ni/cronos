
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm, CareerForm,ClassroomForm
from core.registration.models import Departament, Career, Grupos, Classroom
from core.user.mixins import ValidatePermissionRequiredMixin
from core.utilities import validate_delete

entity = 'Aulas'


class ClassroomListView(ValidatePermissionRequiredMixin, ListView):
    model = Classroom
    template_name = 'classroom/list.html'
    permission_required = 'view_classroom'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [c.toLIST() for c in Classroom.objects.select_related()]

            elif action == 'delete':
                # Validamos si el usuario cuenta con el permiso de eliminar el registor
                if validate_delete(self.permission_required):
                    cli = Classroom.objects.get(id=request.POST['id'])
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
        context['title'] = 'Listado de Aulas'
        context['entity'] = entity
        context['create_url'] = reverse_lazy('classroom_add')
        context['list_url'] = reverse_lazy('classroom_list')
        return context


class ClassroomCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'Classroom/create.html'
    success_url = reverse_lazy('Classroom_list')
    url_redirect = success_url
    permission_required = 'add_classroom'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Aula'
        context['entity'] = entity
        context['list_url'] = reverse_lazy('classroom_list')
        context['action'] = 'add'
        return context


class ClassroomChangeView(ValidatePermissionRequiredMixin, UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classroom/create.html'
    success_url = reverse_lazy('classroom_list')
    url_redirect = success_url
    permission_required = 'change_classroom'

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
        context['title'] = 'Editar classrom'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
