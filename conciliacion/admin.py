from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Balance, DatosFactura, InProyecto, InContabilidad, FormaPago, TablaQuincenal, TablaMensual, TablaSubsidioQ, TablaSubsidioM, Comprobante, FactorIntegracion, DatosPatronIMSS, DatosObrero

# Register your models here.

#admin.site.register(InvoiceRecibidas)
"""
@admin.register(InvoiceRecibidas)
class InvoiceAdmin(admin.ModelAdmin):    
    list_display = ('Estado_SAT', 'Fecha_Emision', 'Fecha_Timbrado', 'UUID', 'RFC_Receptor', 'Nombre_Receptor', 'UsoCFDI', 'SubTotal', 'Total', 'Moneda', 'FormaDePago', 'Metodo_de_Pago', 'timestamp')
    
@admin.register(InvoiceEmitidas)
#class InvoiceAdmin(ImportExportModelAdmin):
class InvoiceEmitidasAdmin(admin.ModelAdmin):    
    list_display = ('Estado_SAT', 'Fecha_Emision', 'Fecha_Timbrado', 'UUID', 'RFC_Receptor', 'Nombre_Receptor', 'UsoCFDI', 'SubTotal', 'Total', 'Moneda', 'Forma_De_Pago', 'Metodo_de_Pago', 'timestamp')
"""    
@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('Cuenta', 'Nombre', 'Deudor_1', 'Cargos', 'Abonos', 'Deudor_2', 'timestamp')

@admin.register(DatosFactura)
class DatosFacturaAdmin(admin.ModelAdmin):
    list_display = ("ProyectoCont", "Contabilidad", "FechaPago", "FormaPago", "Notas", "idUsuario", "UUIDInt")
    
@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    pass

@admin.register(InProyecto)
class InProyectoAdmin(admin.ModelAdmin):
    pass

@admin.register(InContabilidad)
class InContabilidadAdmin(admin.ModelAdmin):
    pass

@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    pass

@admin.register(TablaQuincenal)
#class TablaQuincenalAdmin(admin.ModelAdmin):
class TablaQuincenalAdmin(ImportExportModelAdmin):
    list_display = ("LimiteInferior", "LimiteSuperior", "CuotaFija", "PorcExcedente")

@admin.register(TablaMensual)
class TablaMensualAdmin(ImportExportModelAdmin):
    list_display = ("LimiteInferior", "LimiteSuperior", "CuotaFija", "PorcExcedente")
    
@admin.register(TablaSubsidioQ)
class TablaSubsidioQAdmin(ImportExportModelAdmin):
    list_display = ("LimiteInferior", "LimiteSuperior", "SubsidioAlEmpleo")
    
@admin.register(TablaSubsidioM)
class TablaSubsidioMAdmin(ImportExportModelAdmin):
    list_display = ("LimiteInferior", "LimiteSuperior", "SubsidioAlEmpleo")

@admin.register(FactorIntegracion)
class FactorIntegracionAdmin(ImportExportModelAdmin):
    list_display = ("Aguinaldo", "PVacacional", "DVacaciones", "Antiguedad")

@admin.register(DatosPatronIMSS)
class DatosPatronIMSSAdmin(ImportExportModelAdmin):
    list_display = ('CuotaFija', 'ExcedentePatronal', 'Prestaciones', 'GMPP', 'Invalidez', 'Guarderias', 'Retiro', 'CEAV', 'ACVPatronal')

@admin.register(DatosObrero)
class DatosObreroAdmin(ImportExportModelAdmin):
    list_display = ('ExcedenteObrero', 'PrestacionesObrero', 'GMPO', 'RiesgosTrabajo', 'InvalidezVO', 'CEAVObrero')