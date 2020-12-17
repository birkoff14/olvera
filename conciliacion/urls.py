from django.urls import path

from conciliacion import views

urlpatterns = [
    path('', views.login, name='login'),
    path('menu', views.menu, name='menu'),
    path('logout', views.logout, name='logout'),
    path('clientes', views.customers, name='clientes'),
    path('invoice', views.invoice, name='invoice'),

    #path('export/', views.export_data, name='export'),

]