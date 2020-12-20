from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Invoice 

# Register your models here.

#admin.site.register(Invoice)

@admin.register(Invoice)
#class InvoiceAdmin(ImportExportModelAdmin):
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('Estado_SAT', 'Fecha_Emision', 'Fecha_Timbrado', 'UUID', 'RFC_Receptor', 'Nombre_Receptor', 'UsoCFDI', 'SubTotal', 'Total', 'Moneda', 'Forma_De_Pago', 'Metodo_de_Pago', 'timestamp')

class ExportInvoiceAdmin(ImportExportModelAdmin):
    pass