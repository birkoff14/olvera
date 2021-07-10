from django.urls import path
from django.contrib import admin

from conciliacion import views
from .views import BasicListView
from .models import Balance

urlpatterns = [
    path("", views.login, name="login"),
    path("menu", views.menu, name="menu"),
    path("logout", views.logout, name="logout"),
    path("clientes", views.customers, name="clientes"),
    path("invoice", views.invoice, name="invoice"),
    path("receipts", views.receipts, name="receipts"),
    path("balance", views.impConciliacion, name="balance"),
    path("emitidas", views.repEmitidas, name="emitidas"),
    path("recibidas", views.repRecibidas, name="recibidas"),
    path("conciliacion", views.conciliacion, name="conciliacion"),
    # path('conciliacion/<str:cuenta>/<str:campo_1>/<str:campo_2>/<str:tabla>/<str:title_1>/<str:title_2>', views.conciliacion, name='conciliacion'),
    path(
        "export/<str:cuenta>/<str:campo_1>/<str:campo_2>/<str:tabla>/<str:title_1>/<str:title_2>",
        views.export_data,
        name="export",
    ),
    path("impbalanza", views.impbalanza, name="impbalanza"),
    path("delete/<str:balanza_id>", views.delete_balanza),
    path("deletefactem/<int:factemitidas_id>", views.delete_factemitidas),
    path("deletefactrec/<int:factrecibidas_id>", views.delete_factrecibidas),
    path("pagoprov", views.pagoprov, name="pagoprov"),
    path("country-list/", BasicListView.as_view(model=Balance), name="country_list"),
    path("invoiceDetail/<str:Rfc>/<str:Periodo>/<str:Mes>/<str:Moneda>",views.invoiceDetail,name="invoiceDetail"),
    #path("detailFact/<str:UUIDInt>/<str:RFC>/<str:Periodo>/<str:Mes>/<str:Moneda>", views.detailFact, name="detailFact"),
    path("detailFact/<str:UUIDInt>", views.detailFact, name="detailFact"),
    path("parcialidades", views.parcialidades, name="parcialidades")
]


admin.site.site_header = 'Olvera Contadores'