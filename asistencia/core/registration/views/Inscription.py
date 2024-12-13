from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.registration.forms import DepartamentForm, CareerForm, GroupForm,InscriptionForm
from core.registration.models import Departament, Career, Grupos, Inscription
from core.user.mixins import ValidatePermissionRequiredMixin
from core.utilities import validate_delete

entity = 'inscripcion'


class InscriptionListView(ValidatePermissionRequiredMixin, ListView):
    model = Inscription
    template_name = 'Inscription/list.html'
    permission_required = 'view_inscripcion'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [g.toLIST() for g in Inscription.objects.all()]


            elif action == 'delete':
                # Validamos si el usuario cuenta con el permiso de eliminar el registor
                if validate_delete(self.permission_required):
                    cli = Inscription.objects.get(id=request.POST['id'])
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
        context['title'] = 'Listado de inscripciones'
        context['entity'] = entity
        context['create_url'] = reverse_lazy('Inscription_add')
        context['list_url'] = reverse_lazy('Inscription_list')
        return context


class InscriptionCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Inscription
    form_class = InscriptionForm
    template_name = 'Inscription/create.html'
    success_url = reverse_lazy('Inscription_list')
    url_redirect = success_url
    permission_required = 'add_inscripcion'

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
        context['title'] = 'Crear inscripcion'
        context['entity'] = entity
        context['list_url'] = reverse_lazy('Inscription_lis')
        context['action'] = 'add'
        return context


class InscriptionChangeView(ValidatePermissionRequiredMixin, UpdateView):
    model = Inscription
    form_class = InscriptionForm
    template_name = 'Inscription/create.html'
    success_url = reverse_lazy('Inscription_list')
    url_redirect = success_url
    permission_required = 'change_inscripcion'

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
        context['title'] = 'Editar inscripcion'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

