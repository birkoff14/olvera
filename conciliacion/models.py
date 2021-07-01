from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

################## Clases anteriores


class InvoiceEmitidas(models.Model):
    Verificado_ó_Asoc = models.CharField(max_length=150, blank=True)
    Estado_SAT = models.CharField(max_length=150, blank=True)
    Version = models.CharField(max_length=150, blank=True)
    Tipo = models.CharField(max_length=150, blank=True)
    Fecha_Emision = models.CharField(max_length=150, blank=True)
    Fecha_Timbrado = models.CharField(max_length=150, blank=True)
    EstadoPago = models.CharField(max_length=150, blank=True)
    FechaPago = models.CharField(max_length=150, blank=True)
    Serie = models.CharField(max_length=150, blank=True)
    Folio = models.CharField(max_length=150, blank=True)
    UUID = models.CharField(max_length=150, blank=True)
    UUID_Relacion = models.CharField(max_length=150, blank=True)
    RFC_Emisor = models.CharField(max_length=150, blank=True)
    Nombre_Emisor = models.CharField(max_length=150, blank=True)
    LugarDeExpedicion = models.CharField(max_length=150, blank=True)
    RFC_Receptor = models.CharField(max_length=150, blank=True)
    Nombre_Receptor = models.CharField(max_length=150, blank=True)
    ResidenciaFiscal = models.CharField(max_length=150, blank=True)
    NumRegIdTrib = models.CharField(max_length=150, blank=True)
    UsoCFDI = models.CharField(max_length=150, blank=True)
    SubTotal = models.CharField(max_length=150, blank=True)
    Descuento = models.CharField(max_length=150, blank=True)
    Total_IEPS = models.CharField(max_length=150, blank=True)
    IVA_16 = models.CharField(max_length=150, blank=True)
    Retenido_IVA = models.CharField(max_length=150, blank=True)
    Retenido_ISR = models.CharField(max_length=150, blank=True)
    ISH = models.CharField(max_length=150, blank=True)
    Total = models.CharField(max_length=150, blank=True)
    TotalOriginal = models.CharField(max_length=150, blank=True)
    Total_Trasladados = models.CharField(max_length=150, blank=True)
    Total_Retenidos = models.CharField(max_length=150, blank=True)
    Total_LocalTrasladado = models.CharField(max_length=150, blank=True)
    Total_LocalRetenido = models.CharField(max_length=150, blank=True)
    Complemento = models.CharField(max_length=150, blank=True)
    Moneda = models.CharField(max_length=150, blank=True)
    Tipo_De_Cambio = models.CharField(max_length=150, blank=True)
    Forma_De_Pago = models.CharField(max_length=150, blank=True)
    Metodo_de_Pago = models.CharField(max_length=150, blank=True)
    NumCtaPago = models.CharField(max_length=150, blank=True)
    Condicion_de_Pago = models.CharField(max_length=150, blank=True)
    Conceptos = models.CharField(max_length=150, blank=True)
    Combustible = models.CharField(max_length=150, blank=True)
    IEPS_3 = models.CharField(max_length=150, blank=True)
    IEPS_6 = models.CharField(max_length=150, blank=True)
    IEPS_7 = models.CharField(max_length=150, blank=True)
    IEPS_8 = models.CharField(max_length=150, blank=True)
    IEPS_9 = models.CharField(max_length=150, blank=True)
    IEPS_265 = models.CharField(max_length=150, blank=True)
    IEPS_30 = models.CharField(max_length=150, blank=True)
    IEPS_53 = models.CharField(max_length=150, blank=True)
    IEPS_160 = models.CharField(max_length=150, blank=True)
    Archivo_XML = models.CharField(max_length=150, blank=True)
    Direccion_Emisor = models.CharField(max_length=150, blank=True)
    Localidad_Emisor = models.CharField(max_length=150, blank=True)
    Direccion_Receptor = models.CharField(max_length=150, blank=True)
    Localidad_Receptor = models.CharField(max_length=150, blank=True)
    IVA_8 = models.CharField(max_length=150, blank=True)
    IEPS_304 = models.CharField(max_length=150, blank=True)
    IVA_Ret_6 = models.CharField(max_length=150, blank=True)
    AÑO_Facturado = models.CharField(max_length=150, blank=True)
    Mes_Facturado = models.CharField(max_length=150, blank=True)
    Proyecto = models.CharField(max_length=150, blank=True)
    Evento = models.CharField(max_length=150, blank=True)
    SOCIO_EVENTO = models.CharField(max_length=150, blank=True)
    NOMBRE_EVENTO = models.CharField(max_length=150, blank=True)
    Forma_Cobro = models.CharField(max_length=150, blank=True)
    ASOCIADOS_NO_ASOCIADOS = models.CharField(max_length=150, blank=True)
    Año_cobro = models.CharField(max_length=150, blank=True)
    Mes_Cobro = models.CharField(max_length=150, blank=True)
    NOTAS = models.CharField(max_length=150, blank=True)
    FOLIO_2 = models.CharField(max_length=150, blank=True)
    COMPLEMENTO_DE_PAGO = models.CharField(max_length=150, blank=True)
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
    Verificado_ó_Asoc = models.CharField(max_length=150, blank=True)
    Estado_SAT = models.CharField(max_length=150, blank=True)
    Version = models.CharField(max_length=150, blank=True)
    Tipo = models.CharField(max_length=150, blank=True)
    Fecha_Emision = models.CharField(max_length=150, blank=True)
    Fecha_Timbrado = models.CharField(max_length=150, blank=True)
    EstadoPago = models.CharField(max_length=150, blank=True)
    FechaPago = models.CharField(max_length=150, blank=True)
    Serie = models.CharField(max_length=150, blank=True)
    Folio = models.CharField(max_length=150, blank=True)
    UUID = models.CharField(max_length=150, blank=True)
    UUID_Relacion = models.CharField(max_length=150, blank=True)
    RFC_Emisor = models.CharField(max_length=150, blank=True)
    Nombre_Emisor = models.CharField(max_length=150, blank=True)
    LugarDeExpedicion = models.CharField(max_length=150, blank=True)
    RFC_Receptor = models.CharField(max_length=150, blank=True)
    Nombre_Receptor = models.CharField(max_length=150, blank=True)
    ResidenciaFiscal = models.CharField(max_length=150, blank=True)
    NumRegIdTrib = models.CharField(max_length=150, blank=True)
    UsoCFDI = models.CharField(max_length=150, blank=True)
    SubTotal = models.CharField(max_length=150, blank=True)
    Descuento = models.CharField(max_length=150, blank=True)
    Total_IEPS = models.CharField(max_length=150, blank=True)
    IVA_16 = models.CharField(max_length=150, blank=True)
    Retenido_IVA = models.CharField(max_length=150, blank=True)
    Retenido_ISR = models.CharField(max_length=150, blank=True)
    ISH = models.CharField(max_length=150, blank=True)
    Total = models.CharField(max_length=150, blank=True)
    TotalOriginal = models.CharField(max_length=150, blank=True)
    TotalTrasladados = models.CharField(max_length=150, blank=True)
    Total_Retenidos = models.CharField(max_length=150, blank=True)
    Total_LocalTrasladado = models.CharField(max_length=150, blank=True)
    Total_LocalRetenido = models.CharField(max_length=150, blank=True)
    Complemento = models.CharField(max_length=150, blank=True)
    Moneda = models.CharField(max_length=150, blank=True)
    Tipo_De_Cambio = models.CharField(max_length=150, blank=True)
    FormaDePago = models.CharField(max_length=150, blank=True)
    Metodo_de_Pago = models.CharField(max_length=150, blank=True)
    NumCtaPago = models.CharField(max_length=150, blank=True)
    Condicion_de_Pago = models.CharField(max_length=150, blank=True)
    Conceptos = models.CharField(max_length=150, blank=True)
    Combustible = models.CharField(max_length=150, blank=True)
    IEPS_3 = models.CharField(max_length=150, blank=True)
    IEPS_6 = models.CharField(max_length=150, blank=True)
    IEPS_7 = models.CharField(max_length=150, blank=True)
    IEPS_8 = models.CharField(max_length=150, blank=True)
    IEPS_9 = models.CharField(max_length=150, blank=True)
    IEPS_265 = models.CharField(max_length=150, blank=True)
    IEPS_30 = models.CharField(max_length=150, blank=True)
    IEPS_53 = models.CharField(max_length=150, blank=True)
    IEPS_160 = models.CharField(max_length=150, blank=True)
    Archivo_XML = models.CharField(max_length=150, blank=True)
    Direccion_Emisor = models.CharField(max_length=150, blank=True)
    Localidad_Emisor = models.CharField(max_length=150, blank=True)
    Direccion_Receptor = models.CharField(max_length=150, blank=True)
    Localidad_Receptor = models.CharField(max_length=150, blank=True)
    IVA_8 = models.CharField(max_length=150, blank=True)
    IEPS_304 = models.CharField(max_length=150, blank=True)
    IVA_Ret_6 = models.CharField(max_length=150, blank=True)
    AÑO = models.CharField(max_length=150, blank=True)
    MES_FACTURADO = models.CharField(max_length=150, blank=True)
    PROYECTO = models.CharField(max_length=150, blank=True)
    CONTABILIDAD = models.CharField(max_length=150, blank=True)
    ESTATUS_PAGO = models.CharField(max_length=150, blank=True)
    BANCO = models.CharField(max_length=150, blank=True)
    Mes_Pago_BANCO = models.CharField(max_length=150, blank=True)
    AÑO_PAGO_BANCO = models.CharField(max_length=150, blank=True)
    NOTAS = models.CharField(max_length=150, blank=True)
    TIPO_IVA = models.CharField(max_length=150, blank=True)
    DIOT_COEFICIENTE = models.CharField(max_length=150, blank=True)
    DIOT_BASE_16 = models.CharField(max_length=150, blank=True)
    DIOT_IVA = models.CharField(max_length=150, blank=True)
    COMPLEMENTO_DE_PAGO = models.CharField(max_length=150, blank=True)
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
    Cuenta = models.CharField(max_length=150, blank=True)
    Nombre = models.CharField(max_length=150, blank=True)
    Deudor_1 = models.CharField(max_length=150, blank=True)
    Acreedor_1 = models.CharField(max_length=150, blank=True)
    Cargos = models.CharField(max_length=150, blank=True)
    Abonos = models.CharField(max_length=150, blank=True)
    Deudor_2 = models.CharField(max_length=150, blank=True)
    Acreedor_2 = models.CharField(max_length=150, blank=True)
    Mes = models.CharField(max_length=150, blank=True)
    Año = models.CharField(max_length=150, blank=True)
    RFC = models.CharField(max_length=150, blank=True)
    timestamp =models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Fecha")
    last_modified = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Ultima Actualización")


################## Nuevas clases


class Comprobante(models.Model):
    Version = models.CharField(max_length=5, blank=True)
    Serie = models.CharField(max_length=20, blank=True)
    Folio = models.CharField(max_length=50, blank=True)
    Fecha = models.CharField(max_length=25, blank=True)
    FormaPago = models.CharField(max_length=100, blank=True)
    NoCertificado = models.CharField(max_length=50, blank=True)
    SubTotal = models.CharField(max_length=15, blank=True)
    TipoCambio = models.CharField(max_length=15, blank=True)
    Moneda = models.CharField(max_length=50, blank=True)
    Total = models.CharField(max_length=15, blank=True)
    TipoDeComprobante = models.CharField(max_length=10, blank=True)
    MetodoPago = models.CharField(max_length=100, blank=True)
    LugarExpedicion = models.CharField(max_length=250, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class Emisor(models.Model):
    Rfc = models.CharField(max_length=15, blank=True)
    Nombre = models.CharField(max_length=250, blank=True)
    RegimenFiscal = models.CharField(max_length=5, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class Receptor(models.Model):
    Rfc = models.CharField(max_length=15, blank=True)
    Nombre = models.CharField(max_length=250, blank=True)
    UsoCFDI = models.CharField(max_length=5, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class Concepto(models.Model):
    ClaveProdServ = models.CharField(max_length=15, blank=True)
    NoIdentificacion = models.CharField(max_length=50, blank=True)
    Cantidad = models.CharField(max_length=20, blank=True)
    ClaveUnidad = models.CharField(max_length=20, blank=True)
    Unidad = models.CharField(max_length=20, blank=True)
    Descripcion = models.CharField(max_length=2500, blank=True)
    ValorUnitario = models.CharField(max_length=20, blank=True)
    Importe = models.CharField(max_length=20, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class Pago(models.Model):
    FechaPago = models.CharField(max_length=20, blank=True)
    FormaDePagoP = models.CharField(max_length=20, blank=True)
    MonedaP = models.CharField(max_length=20, blank=True)
    Monto = models.CharField(max_length=20, blank=True)
    NumOperacion = models.CharField(max_length=150, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class DoctoRelacionado(models.Model):
    IdDocumento = models.CharField(max_length=50, blank=True)
    Folio = models.CharField(max_length=20, blank=True)
    Serie = models.CharField(max_length=20, blank=True)
    MonedaDR = models.CharField(max_length=20, blank=True)
    MetodoDePagoDR = models.CharField(max_length=20, blank=True)
    NumParcialidad = models.CharField(max_length=20, blank=True)
    ImpSaldoAnt = models.CharField(max_length=20, blank=True)
    ImpPagado = models.CharField(max_length=20, blank=True)
    ImpSaldoInsoluto = models.CharField(max_length=20, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class Impuestos(models.Model):
    TotalImpuestosTrasladados = models.CharField(max_length=20, blank=True)
    TotalImpuestosRetenidos = models.CharField(max_length=20, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class Traslado(models.Model):
    Base = models.CharField(max_length=20, blank=True)
    Impuesto = models.CharField(max_length=20, blank=True)
    TipoFactor = models.CharField(max_length=20, blank=True)
    TasaOCuota = models.CharField(max_length=20, blank=True)
    Importe = models.CharField(max_length=20, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class TimbreFiscalDigital(models.Model):
    Version = models.CharField(max_length=5, blank=True)
    UUID = models.CharField(max_length=150, blank=True)
    FechaTimbrado = models.CharField(max_length=30, blank=True)
    RfcProvCertif = models.CharField(max_length=20, blank=True)
    NoCertificadoSAT = models.CharField(max_length=20, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)
    
class InProyecto(models.Model):
    idTipo = models.AutoField(primary_key=True)
    InProyecto = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.InProyecto
    
class InContabilidad(models.Model):
    idTipo = models.AutoField(primary_key=True)
    InContabilidad = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.InContabilidad

class GaProyecto(models.Model):
    idTipo = models.AutoField(primary_key=True)
    GaProyecto = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.GaProyecto
    
class GaContabilidad(models.Model):
    idTipo = models.AutoField(primary_key=True)
    GaContabilidad = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.GaContabilidad

class DatosFactura(models.Model):
    idDato = models.AutoField(primary_key=True, verbose_name="DatosFactura")
    InProyecto = models.ForeignKey(InProyecto, on_delete=models.CASCADE, null=True, verbose_name="Ingreso proyecto")
    InContabilidad= models.ForeignKey(InContabilidad, on_delete=models.CASCADE, null=True, verbose_name="Ingreso contabilidad")
    GaProyecto = models.ForeignKey(GaProyecto, on_delete=models.CASCADE, null=True, verbose_name="Gasto proyecto")
    GaContabilidad = models.ForeignKey(GaContabilidad, on_delete=models.CASCADE, null=True, verbose_name="Gasto contabilidad")
    idUsuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    UUIDInt = models.CharField(max_length=60, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Fecha")
    
# Nomina


class Nomina(models.Model):
    FechaFinalPago = models.CharField(max_length=50, blank=True)
    FechaInicialPago = models.CharField(max_length=50, blank=True)
    FechaPago = models.CharField(max_length=50, blank=True)
    NumDiasPagados = models.CharField(max_length=50, blank=True)
    TipoNomina = models.CharField(max_length=50, blank=True)
    TotalOtrosPagos = models.CharField(max_length=50, blank=True)
    TotalPercepciones = models.CharField(max_length=50, blank=True)
    Version = models.CharField(max_length=50, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class NEmisor(models.Model):
    RegistroPatronal = models.CharField(max_length=50, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class NReceptor(models.Model):
    Antigüedad = models.CharField(max_length=50, blank=True)
    ClaveEntFed = models.CharField(max_length=50, blank=True)
    Curp = models.CharField(max_length=50, blank=True)
    Departamento = models.CharField(max_length=50, blank=True)
    FechaInicioRelLaboral = models.CharField(max_length=50, blank=True)
    NumEmpleado = models.CharField(max_length=50, blank=True)
    NumSeguridadSocial = models.CharField(max_length=50, blank=True)
    PeriodicidadPago = models.CharField(max_length=50, blank=True)
    Puesto = models.CharField(max_length=50, blank=True)
    RiesgoPuesto = models.CharField(max_length=50, blank=True)
    SalarioBaseCotApor = models.CharField(max_length=50, blank=True)
    SalarioDiarioIntegrado = models.CharField(max_length=50, blank=True)
    Sindicalizado = models.CharField(max_length=50, blank=True)
    TipoContrato = models.CharField(max_length=50, blank=True)
    TipoJornada = models.CharField(max_length=50, blank=True)
    TipoRegimen = models.CharField(max_length=50, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class NPercepciones(models.Model):
    TotalExento = models.CharField(max_length=50, blank=True)
    TotalGravado = models.CharField(max_length=50, blank=True)
    TotalSueldos = models.CharField(max_length=50, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class NPercepcion(models.Model):
    Clave = models.CharField(max_length=50, blank=True)
    Concepto = models.CharField(max_length=50, blank=True)
    ImporteExento = models.CharField(max_length=50, blank=True)
    ImporteGravado = models.CharField(max_length=50, blank=True)
    TipoPercepcion = models.CharField(max_length=50, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class OtroPago(models.Model):
    Clave = models.CharField(max_length=50, blank=True)
    Concepto = models.CharField(max_length=50, blank=True)
    Importe = models.CharField(max_length=50, blank=True)
    TipoOtroPago = models.CharField(max_length=50, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)


class SubsidioAlEmpleo(models.Model):
    SubsidioCausado = models.CharField(max_length=50, blank=True)
    UUIDInt = models.CharField(max_length=60, blank=True)
