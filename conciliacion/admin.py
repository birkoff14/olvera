from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Invoice 

# Register your models here.

@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin):
    fields = ('Estado_SAT', 'Version', 'Tipo', 'Fecha_Emision', 'Fecha_Timbrado', 'Serie', 'Folio', 'UUID', 'RFC_Receptor', 'Nombre_Receptor', 'UsoCFDI', 'SubTotal', 'IVA_16', 'Total', 'Total_Trasladados', 'Moneda', 'Forma_De_Pago', 'Metodo_de_Pago', )