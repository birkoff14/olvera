from django.contrib import admin
#from import_export.admin import ImportExportModelAdmin
from .models import InvoiceEmitidas, InvoiceRecibidas, Balance

# Register your models here.

#admin.site.register(InvoiceRecibidas)
@admin.register(InvoiceRecibidas)
class InvoiceAdmin(admin.ModelAdmin):    
    list_display = ('Estado_SAT', 'Fecha_Emision', 'Fecha_Timbrado', 'UUID', 'RFC_Receptor', 'Nombre_Receptor', 'UsoCFDI', 'SubTotal', 'Total', 'Moneda', 'FormaDePago', 'Metodo_de_Pago', 'timestamp')
    
@admin.register(InvoiceEmitidas)
#class InvoiceAdmin(ImportExportModelAdmin):
class InvoiceEmitidasAdmin(admin.ModelAdmin):    
    list_display = ('Estado_SAT', 'Fecha_Emision', 'Fecha_Timbrado', 'UUID', 'RFC_Receptor', 'Nombre_Receptor', 'UsoCFDI', 'SubTotal', 'Total', 'Moneda', 'Forma_De_Pago', 'Metodo_de_Pago', 'timestamp')
    
@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('Cuenta', 'Nombre', 'Deudor_1', 'Cargos', 'Abonos', 'Deudor_2', 'timestamp')

#class ExportInvoiceAdmin(ImportExportModelAdmin):
#    pass