from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm, CareerForm
from core.registration.models import Departament, Career
from core.user.mixins import ValidatePermissionRequiredMixin
from core.utilities import validate_delete

entity = 'Carreras'

class CareerListView(ValidatePermissionRequiredMixin, ListView):
    model = Departament
    template_name = 'career/list.html'
    permission_required = 'view_carrera'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [d.toLIST() for d in Career.objects.select_related()]


            elif action == 'delete':
                # Validamos si el usuario cuenta con el permiso de eliminar el registor
                if validate_delete(self.permission_required):
                    cli = Departament.objects.get(id=request.POST['id'])
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
        context['title'] = 'Listado de carreras'
        context['entity'] = entity
        context['create_url'] = reverse_lazy('career_add')
        context['list_url'] = reverse_lazy('career_list')

        return context

class CareerCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Departament
    form_class = CareerForm
    template_name = 'career/create.html'
    success_url = reverse_lazy('career_list')
    url_redirect = success_url
    permission_required = 'add_carrera'

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
        context['title'] = 'Crear carrera'
        context['entity'] = entity
        context['list_url'] = reverse_lazy('career_list')
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