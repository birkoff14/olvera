from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid

# Create your models here.

################## Clases anteriores

class InvoiceEmitidas(models.Model):
    Verificado_ó_Asoc = models.CharField(max_length=150, blank=False)
    Estado_SAT = models.CharField(max_length=150, blank=False)
    Version = models.CharField(max_length=150, blank=False)
    Tipo = models.CharField(max_length=150, blank=False)
    Fecha_Emision = models.CharField(max_length=150, blank=False)
    Fecha_Timbrado = models.CharField(max_length=150, blank=False)
    EstadoPago = models.CharField(max_length=150, blank=False)
    FechaPago = models.CharField(max_length=150, blank=False)
    Serie = models.CharField(max_length=150, blank=False)
    Folio = models.CharField(max_length=150, blank=False)
    UUID = models.CharField(max_length=150, blank=False)
    UUID_Relacion = models.CharField(max_length=150, blank=False)
    RFC_Emisor = models.CharField(max_length=150, blank=False)
    Nombre_Emisor = models.CharField(max_length=150, blank=False)
    LugarDeExpedicion = models.CharField(max_length=150, blank=False)
    RFC_Receptor = models.CharField(max_length=150, blank=False)
    Nombre_Receptor = models.CharField(max_length=150, blank=False)
    ResidenciaFiscal = models.CharField(max_length=150, blank=False)
    NumRegIdTrib = models.CharField(max_length=150, blank=False)
    UsoCFDI = models.CharField(max_length=150, blank=False)
    SubTotal = models.CharField(max_length=150, blank=False)
    Descuento = models.CharField(max_length=150, blank=False)
    Total_IEPS = models.CharField(max_length=150, blank=False)
    IVA_16 = models.CharField(max_length=150, blank=False)
    Retenido_IVA = models.CharField(max_length=150, blank=False)
    Retenido_ISR = models.CharField(max_length=150, blank=False)
    ISH = models.CharField(max_length=150, blank=False)
    Total = models.CharField(max_length=150, blank=False)
    TotalOriginal = models.CharField(max_length=150, blank=False)
    Total_Trasladados = models.CharField(max_length=150, blank=False)
    Total_Retenidos = models.CharField(max_length=150, blank=False)
    Total_LocalTrasladado = models.CharField(max_length=150, blank=False)
    Total_LocalRetenido = models.CharField(max_length=150, blank=False)
    Complemento = models.CharField(max_length=150, blank=False)
    Moneda = models.CharField(max_length=150, blank=False)
    Tipo_De_Cambio = models.CharField(max_length=150, blank=False)
    Forma_De_Pago = models.CharField(max_length=150, blank=False)
    Metodo_de_Pago = models.CharField(max_length=150, blank=False)
    NumCtaPago = models.CharField(max_length=150, blank=False)
    Condicion_de_Pago = models.CharField(max_length=150, blank=False)
    Conceptos = models.CharField(max_length=150, blank=False)
    Combustible = models.CharField(max_length=150, blank=False)
    IEPS_3 = models.CharField(max_length=150, blank=False)
    IEPS_6 = models.CharField(max_length=150, blank=False)
    IEPS_7 = models.CharField(max_length=150, blank=False)
    IEPS_8 = models.CharField(max_length=150, blank=False)
    IEPS_9 = models.CharField(max_length=150, blank=False)
    IEPS_265 = models.CharField(max_length=150, blank=False)
    IEPS_30 = models.CharField(max_length=150, blank=False)
    IEPS_53 = models.CharField(max_length=150, blank=False)
    IEPS_160 = models.CharField(max_length=150, blank=False)
    Archivo_XML = models.CharField(max_length=150, blank=False)
    Direccion_Emisor = models.CharField(max_length=150, blank=False)
    Localidad_Emisor = models.CharField(max_length=150, blank=False)
    Direccion_Receptor = models.CharField(max_length=150, blank=False)
    Localidad_Receptor = models.CharField(max_length=150, blank=False)
    IVA_8 = models.CharField(max_length=150, blank=False)
    IEPS_304 = models.CharField(max_length=150, blank=False)
    IVA_Ret_6 = models.CharField(max_length=150, blank=False)
    AÑO_Facturado = models.CharField(max_length=150, blank=False)
    Mes_Facturado = models.CharField(max_length=150, blank=False)
    Proyecto = models.CharField(max_length=150, blank=False)
    Evento = models.CharField(max_length=150, blank=False)
    SOCIO_EVENTO = models.CharField(max_length=150, blank=False)
    NOMBRE_EVENTO = models.CharField(max_length=150, blank=False)
    Forma_Cobro = models.CharField(max_length=150, blank=False)
    ASOCIADOS_NO_ASOCIADOS = models.CharField(max_length=150, blank=False)
    Año_cobro = models.CharField(max_length=150, blank=False)
    Mes_Cobro = models.CharField(max_length=150, blank=False)
    NOTAS = models.CharField(max_length=150, blank=False)
    FOLIO_2 = models.CharField(max_length=150, blank=False)
    COMPLEMENTO_DE_PAGO = models.CharField(max_length=150, blank=False)
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, null=False, blank=False, verbose_name="Fecha"
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        null=False,
        blank=False,
        verbose_name="Ultima Actualización",
    )

class InvoiceRecibidas(models.Model):
    Verificado_ó_Asoc = models.CharField(max_length=150, blank=False)
    Estado_SAT = models.CharField(max_length=150, blank=False)
    Version = models.CharField(max_length=150, blank=False)
    Tipo = models.CharField(max_length=150, blank=False)
    Fecha_Emision = models.CharField(max_length=150, blank=False)
    Fecha_Timbrado = models.CharField(max_length=150, blank=False)
    EstadoPago = models.CharField(max_length=150, blank=False)
    FechaPago = models.CharField(max_length=150, blank=False)
    Serie = models.CharField(max_length=150, blank=False)
    Folio = models.CharField(max_length=150, blank=False)
    UUID = models.CharField(max_length=150, blank=False)
    UUID_Relacion = models.CharField(max_length=150, blank=False)
    RFC_Emisor = models.CharField(max_length=150, blank=False)
    Nombre_Emisor = models.CharField(max_length=150, blank=False)
    LugarDeExpedicion = models.CharField(max_length=150, blank=False)
    RFC_Receptor = models.CharField(max_length=150, blank=False)
    Nombre_Receptor = models.CharField(max_length=150, blank=False)
    ResidenciaFiscal = models.CharField(max_length=150, blank=False)
    NumRegIdTrib = models.CharField(max_length=150, blank=False)
    UsoCFDI = models.CharField(max_length=150, blank=False)
    SubTotal = models.CharField(max_length=150, blank=False)
    Descuento = models.CharField(max_length=150, blank=False)
    Total_IEPS = models.CharField(max_length=150, blank=False)
    IVA_16 = models.CharField(max_length=150, blank=False)
    Retenido_IVA = models.CharField(max_length=150, blank=False)
    Retenido_ISR = models.CharField(max_length=150, blank=False)
    ISH = models.CharField(max_length=150, blank=False)
    Total = models.CharField(max_length=150, blank=False)
    TotalOriginal = models.CharField(max_length=150, blank=False)
    TotalTrasladados = models.CharField(max_length=150, blank=False)
    Total_Retenidos = models.CharField(max_length=150, blank=False)
    Total_LocalTrasladado = models.CharField(max_length=150, blank=False)
    Total_LocalRetenido = models.CharField(max_length=150, blank=False)
    Complemento = models.CharField(max_length=150, blank=False)
    Moneda = models.CharField(max_length=150, blank=False)
    Tipo_De_Cambio = models.CharField(max_length=150, blank=False)
    FormaDePago = models.CharField(max_length=150, blank=False)
    Metodo_de_Pago = models.CharField(max_length=150, blank=False)
    NumCtaPago = models.CharField(max_length=150, blank=False)
    Condicion_de_Pago = models.CharField(max_length=150, blank=False)
    Conceptos = models.CharField(max_length=150, blank=False)
    Combustible = models.CharField(max_length=150, blank=False)
    IEPS_3 = models.CharField(max_length=150, blank=False)
    IEPS_6 = models.CharField(max_length=150, blank=False)
    IEPS_7 = models.CharField(max_length=150, blank=False)
    IEPS_8 = models.CharField(max_length=150, blank=False)
    IEPS_9 = models.CharField(max_length=150, blank=False)
    IEPS_265 = models.CharField(max_length=150, blank=False)
    IEPS_30 = models.CharField(max_length=150, blank=False)
    IEPS_53 = models.CharField(max_length=150, blank=False)
    IEPS_160 = models.CharField(max_length=150, blank=False)
    Archivo_XML = models.CharField(max_length=150, blank=False)
    Direccion_Emisor = models.CharField(max_length=150, blank=False)
    Localidad_Emisor = models.CharField(max_length=150, blank=False)
    Direccion_Receptor = models.CharField(max_length=150, blank=False)
    Localidad_Receptor = models.CharField(max_length=150, blank=False)
    IVA_8 = models.CharField(max_length=150, blank=False)
    IEPS_304 = models.CharField(max_length=150, blank=False)
    IVA_Ret_6 = models.CharField(max_length=150, blank=False)
    AÑO = models.CharField(max_length=150, blank=False)
    MES_FACTURADO = models.CharField(max_length=150, blank=False)
    PROYECTO = models.CharField(max_length=150, blank=False)
    CONTABILIDAD = models.CharField(max_length=150, blank=False)
    ESTATUS_PAGO = models.CharField(max_length=150, blank=False)
    BANCO = models.CharField(max_length=150, blank=False)
    Mes_Pago_BANCO = models.CharField(max_length=150, blank=False)
    AÑO_PAGO_BANCO = models.CharField(max_length=150, blank=False)
    NOTAS = models.CharField(max_length=150, blank=False)
    TIPO_IVA = models.CharField(max_length=150, blank=False)
    DIOT_COEFICIENTE = models.CharField(max_length=150, blank=False)
    DIOT_BASE_16 = models.CharField(max_length=150, blank=False)
    DIOT_IVA = models.CharField(max_length=150, blank=False)
    COMPLEMENTO_DE_PAGO = models.CharField(max_length=150, blank=False)
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, null=False, blank=False, verbose_name="Fecha"
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        null=False,
        blank=False,
        verbose_name="Ultima Actualización",
    )

class Balance(models.Model):
    Cuenta = models.CharField(max_length=150, blank=False)
    Nombre = models.CharField(max_length=150, blank=False)
    Deudor_1 = models.CharField(max_length=150, blank=False)
    Acreedor_1 = models.CharField(max_length=150, blank=False)
    Cargos = models.CharField(max_length=150, blank=False)
    Abonos = models.CharField(max_length=150, blank=False)
    Deudor_2 = models.CharField(max_length=150, blank=False)
    Acreedor_2 = models.CharField(max_length=150, blank=False)
    Mes = models.CharField(max_length=150, blank=False)
    Año = models.CharField(max_length=150, blank=False)
    RFC = models.CharField(max_length=150, blank=False)
    timestamp =models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Fecha")
    last_modified = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Ultima Actualización")
    def __str__(self):
        return self.Cuenta

################## Nuevas clases

class RFCClientes(models.Model):
    Rfc = models.CharField(max_length=20, blank=False)

class Comprobante(models.Model):        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Activo = models.CharField(max_length=20, blank=False)
    TipoEmRe = models.CharField(max_length=10, blank=False)
    Version = models.CharField(max_length=5, blank=False)
    Serie = models.CharField(max_length=20, blank=False)
    Folio = models.CharField(max_length=50, blank=False)
    Fecha = models.DateTimeField()
    FormaPago = models.CharField(max_length=100, blank=False)
    NoCertificado = models.CharField(max_length=50, blank=False)
    SubTotal = models.CharField(max_length=15, blank=False)
    TipoCambio = models.CharField(max_length=15, blank=False)
    Moneda = models.CharField(max_length=50, blank=False)
    Total = models.CharField(max_length=15, blank=False)
    TipoDeComprobante = models.CharField(max_length=10, blank=False)
    MetodoPago = models.CharField(max_length=100, blank=False)
    LugarExpedicion = models.CharField(max_length=250, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Fecha")
    
class Emisor(models.Model):        
    Rfc = models.CharField(max_length=15, blank=False)
    Nombre = models.CharField(max_length=250, blank=False)
    RegimenFiscal = models.CharField(max_length=5, blank=False)   
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True) 

class Receptor(models.Model):        
    Rfc = models.CharField(max_length=15, blank=False)
    Nombre = models.CharField(max_length=250, blank=False)
    UsoCFDI = models.CharField(max_length=5, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)

class Concepto(models.Model):    
    ClaveProdServ = models.CharField(max_length=15, blank=False)
    NoIdentificacion = models.CharField(max_length=50, blank=False)
    Cantidad = models.CharField(max_length=20, blank=False)
    ClaveUnidad = models.CharField(max_length=20, blank=False)
    Unidad = models.CharField(max_length=20, blank=False)
    Descripcion = models.CharField(max_length=2500, blank=False)
    ValorUnitario = models.CharField(max_length=20, blank=False)
    Importe = models.CharField(max_length=20, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)
    
    #UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class Pago(models.Model):
    FechaPago = models.CharField(max_length=20, blank=False)
    FormaDePagoP = models.CharField(max_length=20, blank=False)
    MonedaP = models.CharField(max_length=20, blank=False)
    Monto = models.CharField(max_length=20, blank=False)
    NumOperacion = models.CharField(max_length=150, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class DoctoRelacionado(models.Model):    
    IdDocumento = models.CharField(max_length=50, blank=False)
    Folio = models.CharField(max_length=20, blank=False)
    Serie = models.CharField(max_length=20, blank=False)
    MonedaDR = models.CharField(max_length=20, blank=False)
    MetodoDePagoDR = models.CharField(max_length=20, blank=False)
    NumParcialidad = models.CharField(max_length=20, blank=False)
    ImpSaldoAnt = models.CharField(max_length=20, blank=False)
    ImpPagado = models.CharField(max_length=20, blank=False)
    ImpSaldoInsoluto = models.CharField(max_length=20, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)
    #UUIDInt = models.UUIDField(default=uuid.uuid4, editable=False)
    #UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class Impuestos(models.Model):
    TotalImpuestosTrasladados = models.CharField(max_length=20, blank=False)
    TotalImpuestosRetenidos = models.CharField(max_length=20, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class Traslado(models.Model):
    Base = models.CharField(max_length=20, blank=False)
    Impuesto = models.CharField(max_length=20, blank=False)
    TipoFactor = models.CharField(max_length=20, blank=False)
    TasaOCuota = models.CharField(max_length=20, blank=False)
    Importe = models.CharField(max_length=20, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class TimbreFiscalDigital(models.Model):
    Version = models.CharField(max_length=5, blank=False)
    UUID = models.CharField(max_length=150, blank=False)
    FechaTimbrado = models.CharField(max_length=30, blank=False)
    RfcProvCertif = models.CharField(max_length=20, blank=False)
    NoCertificadoSAT = models.CharField(max_length=20, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)
    
class InProyecto(models.Model):
    idTipo = models.AutoField(primary_key=True)
    InProyecto = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return self.InProyecto
    
class InContabilidad(models.Model):
    idTipo = models.AutoField(primary_key=True)
    InContabilidad = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return self.InContabilidad

class GaProyecto(models.Model):
    idTipo = models.AutoField(primary_key=True)
    GaProyecto = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return self.GaProyecto
    
class GaContabilidad(models.Model):
    idTipo = models.AutoField(primary_key=True)
    GaContabilidad = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return self.GaContabilidad
    
class FormaPago(models.Model):
    idTipo = models.AutoField(primary_key=True)
    FormaPago = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return self.FormaPago

class DatosFactura(models.Model):
    idDato = models.AutoField(primary_key=True, verbose_name="ID")
    ProyectoCont = models.ForeignKey(InProyecto, on_delete=models.CASCADE, null=True, verbose_name="Proyectos")    
    Contabilidad = models.ForeignKey(InContabilidad, on_delete=models.CASCADE, null=True, verbose_name="Contabilidad")
    #GaProyecto = models.ForeignKey(GaProyecto, on_delete=models.CASCADE, null=True, verbose_name="Gasto proyecto")
    #GaContabilidad = models.ForeignKey(GaContabilidad, on_delete=models.CASCADE, null=True, verbose_name="Gasto contabilidad")
    FechaPago = models.CharField(max_length=50, blank=False)
    FormaPago = models.ForeignKey(FormaPago, on_delete=models.CASCADE, null=True, verbose_name="Forma de pago")
    Notas = models.CharField(max_length=5000, blank=False)
    CuentaContable = models.CharField(max_length=50, blank=False)
    #CuentaContable = models.ForeignKey(Balance, on_delete=models.CASCADE, null=True, verbose_name="Cuenta Contable")
    idUsuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Fecha")
    
# Nomina

class Nomina(models.Model):
    FechaFinalPago = models.CharField(max_length=50, blank=False)
    FechaInicialPago = models.CharField(max_length=50, blank=False)
    FechaPago = models.CharField(max_length=50, blank=False)
    NumDiasPagados = models.CharField(max_length=50, blank=False)
    TipoNomina = models.CharField(max_length=50, blank=False)
    TotalOtrosPagos = models.CharField(max_length=50, blank=False)
    TotalPercepciones = models.CharField(max_length=50, blank=False)
    Version = models.CharField(max_length=50, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class NEmisor(models.Model):
    RegistroPatronal = models.CharField(max_length=50, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class NReceptor(models.Model):
    Antigüedad = models.CharField(max_length=50, blank=False)
    ClaveEntFed = models.CharField(max_length=50, blank=False)
    Curp = models.CharField(max_length=50, blank=False)
    Departamento = models.CharField(max_length=50, blank=False)
    FechaInicioRelLaboral = models.CharField(max_length=50, blank=False)
    NumEmpleado = models.CharField(max_length=50, blank=False)
    NumSeguridadSocial = models.CharField(max_length=50, blank=False)
    PeriodicidadPago = models.CharField(max_length=50, blank=False)
    Puesto = models.CharField(max_length=50, blank=False)
    RiesgoPuesto = models.CharField(max_length=50, blank=False)
    SalarioBaseCotApor = models.CharField(max_length=50, blank=False)
    SalarioDiarioIntegrado = models.CharField(max_length=50, blank=False)
    Sindicalizado = models.CharField(max_length=50, blank=False)
    TipoContrato = models.CharField(max_length=50, blank=False)
    TipoJornada = models.CharField(max_length=50, blank=False)
    TipoRegimen = models.CharField(max_length=50, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class NPercepciones(models.Model):
    TotalExento = models.CharField(max_length=50, blank=False)
    TotalGravado = models.CharField(max_length=50, blank=False)
    TotalSueldos = models.CharField(max_length=50, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class NPercepcion(models.Model):
    Clave = models.CharField(max_length=50, blank=False)
    Concepto = models.CharField(max_length=50, blank=False)
    ImporteExento = models.CharField(max_length=50, blank=False)
    ImporteGravado = models.CharField(max_length=50, blank=False)
    TipoPercepcion = models.CharField(max_length=50, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)


class OtroPago(models.Model):
    Clave = models.CharField(max_length=50, blank=False)
    Concepto = models.CharField(max_length=50, blank=False)
    Importe = models.CharField(max_length=50, blank=False)
    TipoOtroPago = models.CharField(max_length=50, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)

class SubsidioAlEmpleo(models.Model):
    SubsidioCausado = models.CharField(max_length=50, blank=False)
    UUIDInt = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=True)
    
class TablaQuincenal(models.Model):
    LimiteInferior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    LimiteSuperior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    CuotaFija = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    PorcExcedente = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    
class TablaMensual(models.Model):
    LimiteInferior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    LimiteSuperior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    CuotaFija = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    PorcExcedente = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    
class TablaSubsidioQ(models.Model):
    LimiteInferior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    LimiteSuperior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    SubsidioAlEmpleo = models.DecimalField(max_digits=19, decimal_places=4, blank=False)

class TablaSubsidioM(models.Model):
    LimiteInferior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    LimiteSuperior = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    SubsidioAlEmpleo = models.DecimalField(max_digits=19, decimal_places=4, blank=False)

class FactorIntegracion(models.Model):
    Aguinaldo = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    PVacacional = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    DVacaciones = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    Antiguedad = models.DecimalField(max_digits=19, decimal_places=4, blank=False)

class UMA(models.Model):
    SDI = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    UMA = models.DecimalField(max_digits=19, decimal_places=4, blank=False)

class DatosPatronIMSS(models.Model): 
    CuotaFija = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    ExcedentePatronal = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    Prestaciones = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    GMPP = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    Invalidez = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    Guarderias = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    Retiro = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    CEAV = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    ACVPatronal = models.DecimalField(max_digits=19, decimal_places=4, blank=False)

class DatosObrero(models.Model):
    ExcedenteObrero = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    PrestacionesObrero = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    GMPO = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    RiesgosTrabajo = models.DecimalField(max_digits=19, decimal_places=7, blank=False)
    InvalidezVO = models.DecimalField(max_digits=19, decimal_places=4, blank=False)
    CEAVObrero = models.DecimalField(max_digits=19, decimal_places=4, blank=False)


class Definitivos(models.Model):
    RFC01 = models.CharField(max_length=250, blank=False)
    Nombre02 = models.CharField(max_length=500, blank=False)
    Situacion03 = models.CharField(max_length=250, blank=False)
    NoPresuncion04 = models.CharField(max_length=250, blank=False)
    FechaPublicacion05 = models.CharField(max_length=250, blank=False)
    SATPresunto06 = models.CharField(max_length=250, blank=False)
    NoFechaDOF07 = models.CharField(max_length=250, blank=False)
    PublicacionDOF08 = models.CharField(max_length=250, blank=False)
    SATDesvirtuados09 = models.CharField(max_length=250, blank=False)
    NoFechaGlobalDOF10 = models.CharField(max_length=250, blank=False)
    PublicacionDOFdesvirtuados11 = models.CharField(max_length=250, blank=False)
    NoFechaDefinitivosSAT12 = models.CharField(max_length=250, blank=False)
    SATPaginaDefinitivos13 = models.CharField(max_length=250, blank=False)
    NoFechaGlobalDefinitivosDOF14 = models.CharField(max_length=250, blank=False)
    PublicacionDOFDefinitivos15 = models.CharField(max_length=250, blank=False)
    SentenciaSAT16 = models.CharField(max_length=250, blank=False)
    SentenciaFavorableSAT17 = models.CharField(max_length=250, blank=False)
    OficioGlobalDOF18 = models.CharField(max_length=250, blank=False)
    PublicacionDOFSentenciaFavorable19 = models.CharField(max_length=250, blank=False)


class NoLocalizados(models.Model):
    RFC = models.CharField(max_length=50, blank=False)
    RazonSocial = models.CharField(max_length=500, blank=False)
    TipoPersona = models.CharField(max_length=50, blank=False)
    Supuesto = models.CharField(max_length=50, blank=False)
    FechaPrimera = models.CharField(max_length=50, blank=False)
    Entidad = models.CharField(max_length=50, blank=False)