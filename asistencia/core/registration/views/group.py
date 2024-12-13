from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm, CareerForm, GroupForm
from core.registration.models import Departament, Career, Grupos
from core.user.mixins import ValidatePermissionRequiredMixin
from core.utilities import validate_delete

entity = 'Grupos'


class GroupListView(ValidatePermissionRequiredMixin, ListView):
    model = Grupos
    template_name = 'group/list.html'
    permission_required = 'view_grupo'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [g.toLIST() for g in Grupos.objects.all()]


            elif action == 'delete':
                # Validamos si el usuario cuenta con el permiso de eliminar el registor
                if validate_delete(self.permission_required):
                    cli = Grupos.objects.get(id=request.POST['id'])
                    cli.delete()
                else:
                    data['error'] = 'No tiene permiso para realizar la siguiente acción'

            else:
                data['error'] = 'Ha ocurrido un error con el action'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de grupos'
        context['entity'] = entity
        context['create_url'] = reverse_lazy('group_add')
        context['list_url'] = reverse_lazy('group_list')
        return context


class GroupCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Grupos
    form_class = GroupForm
    template_name = 'group/create.html'
    success_url = reverse_lazy('group_list')
    url_redirect = success_url
    permission_required = 'add_grupo'

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
        context['title'] = 'Crear grupo'
        context['entity'] = entity
        context['list_url'] = reverse_lazy('group_list')
        context['action'] = 'add'
        return context


class GroupChangeView(ValidatePermissionRequiredMixin, UpdateView):
    model = Grupos
    form_class = GroupForm
    template_name = 'group/create.html'
    success_url = reverse_lazy('group_list')
    url_redirect = success_url
    permission_required = 'change_grupo'

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
        context['title'] = 'Editar grupo'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

