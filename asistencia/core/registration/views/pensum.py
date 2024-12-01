from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm, PensumForm
from core.registration.models import Departament, Pensum
from core.user.mixins import ValidatePermissionRequiredMixin
from core.utilities import validate_delete

entity = 'Pensum'

class PensumListView(ValidatePermissionRequiredMixin, ListView):
    model = Pensum
    template_name = 'pensum/list.html'
    permission_required = 'view_pensum'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [d.toLIST() for d in Pensum.objects.select_related()]

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
        context['title'] = 'Listado de pensum'
        context['create_url'] = reverse_lazy('pensum_add')
        context['list_url'] = reverse_lazy('pensum_list')
        context['entity'] = 'Pensum'

        return context

class PensumCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Pensum
    form_class = PensumForm
    template_name = 'pensum/create.html'
    success_url = reverse_lazy('pensum_list')
    url_redirect = success_url
    permission_required = 'add_pensum'

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
        context['title'] = 'Crear pensum'
        context['list_url'] = reverse_lazy('pensum_list')
        context['entity'] = entity
        context['action'] = 'add'
        return context


class PensumChangeView(ValidatePermissionRequiredMixin, UpdateView):
    model = Pensum
    form_class = PensumForm
    template_name = 'pensum/create.html'
    success_url = reverse_lazy('pensum_list')
    url_redirect = success_url
    permission_required = 'change_pensum'

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
        context['title'] = 'Editar pensum'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context