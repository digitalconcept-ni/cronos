from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm
from core.registration.models import Departament
from core.user.mixins import ValidatePermissionRequiredMixin
from core.utilities import validate_delete


class DepartamentListView(ValidatePermissionRequiredMixin, ListView):
    model = Departament
    template_name = 'departament/list.html'
    permission_required = 'view_departamento'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [d.toLIST() for d in Departament.objects.select_related()]


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
        context['title'] = 'Listado de departamentos'
        context['create_url'] = reverse_lazy('departament_add')
        context['list_url'] = reverse_lazy('departament_list')
        context['entity'] = 'Departamentos'

        return context

class DepartamentCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Departament
    form_class = DepartamentForm
    template_name = 'departament/create.html'
    success_url = reverse_lazy('departament_list')
    url_redirect = success_url
    permission_required = 'add_departamento'

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
        context['title'] = 'Listado de departamentos'
        context['list_url'] = reverse_lazy('departament_list')
        context['entity'] = 'Departamentos'
        context['action'] = 'add'
        return context


class DepartamentChange(ValidatePermissionRequiredMixin, UpdateView):
    model = Departament
    form_class = DepartamentForm
    template_name = 'departament/create.html'
    success_url = reverse_lazy('departament_list')
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
                form.save()
                data = {'info': 'Datos cambiados correctamente'}

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de departamentos'
        context['entity'] = 'Departamentos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context