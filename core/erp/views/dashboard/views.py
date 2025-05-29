from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from datetime import datetime
from core.erp.models import *
from random import randint
from datetime import datetime


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        current_time = datetime.now()  # Obtiene la hora actual
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                data = {
                    'name': 'Ventas por mes',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_month()
                }
            elif action == 'get_graph_sales_products_year_month':
                data = {
                    'name': 'Porcentaje de Producto Vendido: ',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_month()
                }
            elif action == 'get_graph_online':
                data = {'y': randint(1, 100)}
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_sales_products_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Product.objects.all():
                # sales for months ->
                # total = DetSale.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
                #                                prod_id=p.id).aggregate(
                #     r=Coalesce(Sum('subtotal'), 0)).get('r')

                # sales for year
                total = DetSale.objects.filter(sale__date_joined__year=year, prod_id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.name,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        current_time = datetime.now()
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['title'] = 'Pagina Principal'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        context['current_time'] = datetime.now()
        if current_time.hour < 12:
            context['greeting'] = '¡Buenos días!'
        elif current_time.hour < 18:
            context['greeting'] = '¡Buenas tardes!'
        else:
            context['greeting'] = '¡Buenas noches!'
        return context
