from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm, CareerForm, SubjectForm
from core.registration.models import Departament, Career, Subject
from core.user.mixins import ValidatePermissionRequiredMixin
from core.utilities import validate_delete

entity = 'Asignatura'

class SubjectListView(ValidatePermissionRequiredMixin, ListView):
    model = Subject
    template_name = 'subject/list.html'
    permission_required = 'view_asignatura'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [d.toLIST() for d in Subject.objects.select_related()]


            elif action == 'delete':
                # Validamos si el usuario cuenta con el permiso de eliminar el registor
                if validate_delete(self.permission_required):
                    cli = Subject.objects.get(id=request.POST['id'])
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
        context['title'] = 'Listado de asignaturas'
        context['entity'] = entity
        context['create_url'] = reverse_lazy('subject_add')
        context['list_url'] = reverse_lazy('subject_list')

        return context

class SubjectCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject/create.html'
    success_url = reverse_lazy('subject_list')
    url_redirect = success_url
    permission_required = 'add_asignatura'

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
        context['title'] = 'Crear Asignatura'
        context['entity'] = entity
        context['list_url'] = reverse_lazy('subject_list')
        context['action'] = 'add'
        return context


class SubjectChangeView(ValidatePermissionRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject/create.html'
    success_url = reverse_lazy('subject_list')
    url_redirect = success_url
    permission_required = 'change_asignatura'

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
        context['title'] = 'Editar asignatura'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context