# Request = Solicitud, pedido
# Response = Respuesta
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.template import Context, Template, loader
from django.template.loader import get_template
from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from config import settings
# from core.branches.models import boxes, send_emails


# from Apps.test import send_email

# class DaschboardView(LoginRequiredMixin, TemplateView):
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def sendEmail(self):
    #     data = len([i for i in SendEmails.objects.filter(send__exact=0)])
    #     return data

    def agrupar_valores_por_clave(self, lista_de_diccionarios):
        # Crear un diccionario para almacenar los valores por clave
        valores_por_clave = {}

        for i in lista_de_diccionarios:
            # Si existe el valor el el diccionario
            if i['branch__name'] in valores_por_clave:
                # valores_por_clave[i['branch__name']][0].append(int(i['status']))
                # valores_por_clave[i['branch__name']].append(int(i['branch__count']))
                if int(i['status']) == 0:
                    valores_por_clave[i['branch__name']][0] = int(i['branch__count'])
                if int(i['status']) == 1:
                    valores_por_clave[i['branch__name']][1] = int(i['branch__count'])
                if int(i['status']) == 2:
                    valores_por_clave[i['branch__name']][2] = int(i['branch__count'])
            else:
                # Si no existe el valor en el diccionario
                if int(i['status']) == 0:
                    valores_por_clave[i['branch__name']] = [int(i['branch__count']), 0, 0]
                if int(i['status']) == 1:
                    valores_por_clave[i['branch__name']] = [0, int(i['branch__count']), 0]
                if int(i['status']) == 2:
                    valores_por_clave[i['branch__name']] = [0, 0, int(i['branch__count'])]

        return valores_por_clave

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         today = datetime.now().date()
    #         data = []
    #         action = request.POST['action']
    #         if action == 'search_data':
    #
    #             # for email in send_emails.objects.all():
    #             #     print(email.toJSON())
    #
    #             query = boxes.objects.all()
    #
    #             # Contador de la cantidad de las cajas para las cards del dia
    #             counter = query.values('status').annotate(total=Count('status')).order_by(
    #                 '-status')
    #
    #             total = counter[0]['total'] + counter[1]['total'] + counter[2]['total']
    #             data.append({
    #                 'complete': counter[0]['total'],
    #                 'revision': counter[1]['total'],
    #                 'pending': counter[2]['total'],
    #                 'total': total,
    #             })
    #
    #             # SECTION TO RECOLLECT THE FIRST 5 BOXES INSERT THE BRANCHES
    #             # uregister = ultimate boxes register to the branches
    #             uregister = query.filter(date_joined=today).order_by('time_joined')[:5]
    #
    #             listUltimateBoxes = []
    #             for j in uregister:
    #                 listUltimateBoxes.append(
    #                     [j.time_joined.strftime('%I:%M:%S %p'), j.branch.name, j.user.username, j.box])
    #
    #             data.append(listUltimateBoxes)
    #
    #             # Informacion de la cantidad de cajas y total de cajas por sucursal
    #             branches = query.values('branch__name', 'status').annotate(Count('branch')).order_by('status')
    #
    #             resultado = self.agrupar_valores_por_clave(branches)
    #             data.append(resultado)
    #         # elif action == 'notification':
    #         #     for i in SendEmails.objects.filter(send__exact=0):
    #         #         data.append(
    #         #             [i.id, i.follow.id, i.follow.user.id, i.follow.box.box, i.follow.user.username,
    #         #              i.follow.date.strftime("%Y-%m-%d - %H:%M:%S"),
    #         #              i.follow.comment, i.follow.box.id])
    #         elif action == 'complete':
    #             # BLOQUE CONSULTA DASCHBOARD DE CAJAS COMPLETAS
    #             u = 0
    #             s = 0
    #             # data = [i.toJSON(u, s) for i in Boxes.objects.filter(status__exact=2)]
    #             # for i in Boxes.objects.filter(status__exact=2):
    #             #     data.append([
    #             #         i.id,
    #             #         i.branch.name,
    #             #         i.box,
    #             #         i.quantity_of_items(),
    #             #         i.status,
    #             #         i.user.username,
    #             #         i.date_joined.strftime("%Y-%m-%d")
    #             #     ])
    #         elif action == 'revision':
    #             # BLOQUE CONSULTA DASCHBOARD DE CAJAS EN REVISION
    #             u = 0
    #             s = 0
    #             # data = [i.toJSON(u, s) for i in Boxes.objects.filter(status__exact=1)]
    #             # for i in Boxes.objects.filter(status__exact=1):
    #             #     data.append([
    #             #         i.id,
    #             #         i.branch.name,
    #             #         i.box,
    #             #         i.quantity_of_items(),
    #             #         i.status,
    #             #         i.user.username,
    #             #         i.date_joined.strftime("%Y-%m-%d")
    #             #     ])
    #         elif action == 'pending':
    #             # BLOQUE CONSULTA DASCHBOARD DE CAJAS PENDIENTES
    #             u = 0
    #             s = 0
    #             # data = [i.toJSON(u, s) for i in Boxes.objects.filter(status__exact=0)]
    #             # for i in Boxes.objects.filter(status__exact=0):
    #             #     data.append([
    #             #         i.id,
    #             #         i.branch.name,
    #             #         i.box,
    #             #         i.quantity_of_items(),
    #             #         i.status,
    #             #         i.user.username,
    #             #         i.date_joined.strftime("%Y-%m-%d")
    #             #     ])
    #         elif action == 'box':
    #             u = 0
    #             s = 0
    #             # branches_id = [i.id for i in Branches.objects.all()]
    #             # boxes = [i.toJSON(u, s) for i in Boxes.objects.all()]
    #             # result = {}  # variable para los resultados
    #             # resultList = []  # para convertir el resultado en listra
    #             # for i in branches_id:
    #             #     for j in boxes:
    #             #         if i == j['branch']:
    #             #             if j['branch_name'] in result:
    #             #                 result[j['branch_name']] += 1
    #             #             else:
    #             #                 result[j['branch_name']] = 1
    #             # for k, v in result.items():  # aqui se logra convertir a una lista para la tabla
    #             #     s += 1
    #             #     resultList.append([k, v])
    #             # data = resultList
    #         # elif action == 'email':
    #         #     data = {}
    #         #     fw_id = int(request.POST['box_id'])
    #         #     info = [i.toJSON() for i in SendEmails.objects.filter(follow_id=fw_id)]
    #         #     response = send_email(info)
    #         #     if response == True:
    #         #         for i in SendEmails.objects.filter(follow_id=fw_id):
    #         #             i.delete()
    #         #
    #         #         email = SendEmails()
    #         #         email.follow_id = fw_id
    #         #         email.send = 1
    #         #         email.save()
    #         #
    #         #         data['info'] = 'Correo enviado correctamente'
    #         #     else:
    #         #         data['error'] = 'ha ocurrido un error al momentos de enviar el correo'
    #         elif action == 'ping':
    #             pass
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Cronos | Dashboard'
        data['action'] = 'search_data'
        data['entity'] = 'Dashboard'
        data['logout'] = reverse_lazy('logout')
        # data['notifications'] = self.sendEmail()
        return data


# class Test(TemplateView):
#     template_name = 'send_email.html'
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         pass
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Select Aninados | Django'
#         return context


# def ping(request):
#     data ={}
#     data['notification'] = len([i for i in SendEmails.objects.filter(send__exact=0)])
#     return JsonResponse(data, safe=False)


"""def dash(request):
    complete = 0
    revision = 0
    pending = 0
    for i in Boxes.objects.all():
        if int(i.status) == 0:
            pending += 1
        elif int(i.status) == 1:
            revision += 1
        else:
            complete += 1
    data = {
        'complete': complete,
        'revision': revision,
        'pending': pending,
    }
    return render(request, 'dashboard.html', data)"""
