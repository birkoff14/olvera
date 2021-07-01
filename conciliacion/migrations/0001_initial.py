# Generated by Django 3.1.4 on 2021-06-30 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cuenta', models.CharField(blank=True, max_length=150)),
                ('Nombre', models.CharField(blank=True, max_length=150)),
                ('Deudor_1', models.CharField(blank=True, max_length=150)),
                ('Acreedor_1', models.CharField(blank=True, max_length=150)),
                ('Cargos', models.CharField(blank=True, max_length=150)),
                ('Abonos', models.CharField(blank=True, max_length=150)),
                ('Deudor_2', models.CharField(blank=True, max_length=150)),
                ('Acreedor_2', models.CharField(blank=True, max_length=150)),
                ('Mes', models.CharField(blank=True, max_length=150)),
                ('Año', models.CharField(blank=True, max_length=150)),
                ('RFC', models.CharField(blank=True, max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Ultima Actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Version', models.CharField(blank=True, max_length=5)),
                ('Serie', models.CharField(blank=True, max_length=20)),
                ('Folio', models.CharField(blank=True, max_length=50)),
                ('Fecha', models.CharField(blank=True, max_length=25)),
                ('FormaPago', models.CharField(blank=True, max_length=100)),
                ('NoCertificado', models.CharField(blank=True, max_length=50)),
                ('SubTotal', models.CharField(blank=True, max_length=15)),
                ('TipoCambio', models.CharField(blank=True, max_length=15)),
                ('Moneda', models.CharField(blank=True, max_length=50)),
                ('Total', models.CharField(blank=True, max_length=15)),
                ('TipoDeComprobante', models.CharField(blank=True, max_length=10)),
                ('MetodoPago', models.CharField(blank=True, max_length=100)),
                ('LugarExpedicion', models.CharField(blank=True, max_length=250)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ClaveProdServ', models.CharField(blank=True, max_length=15)),
                ('NoIdentificacion', models.CharField(blank=True, max_length=50)),
                ('Cantidad', models.CharField(blank=True, max_length=20)),
                ('ClaveUnidad', models.CharField(blank=True, max_length=20)),
                ('Unidad', models.CharField(blank=True, max_length=20)),
                ('Descripcion', models.CharField(blank=True, max_length=2500)),
                ('ValorUnitario', models.CharField(blank=True, max_length=20)),
                ('Importe', models.CharField(blank=True, max_length=20)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='DoctoRelacionado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdDocumento', models.CharField(blank=True, max_length=50)),
                ('Folio', models.CharField(blank=True, max_length=20)),
                ('Serie', models.CharField(blank=True, max_length=20)),
                ('MonedaDR', models.CharField(blank=True, max_length=20)),
                ('MetodoDePagoDR', models.CharField(blank=True, max_length=20)),
                ('NumParcialidad', models.CharField(blank=True, max_length=20)),
                ('ImpSaldoAnt', models.CharField(blank=True, max_length=20)),
                ('ImpPagado', models.CharField(blank=True, max_length=20)),
                ('ImpSaldoInsoluto', models.CharField(blank=True, max_length=20)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Emisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rfc', models.CharField(blank=True, max_length=15)),
                ('Nombre', models.CharField(blank=True, max_length=250)),
                ('RegimenFiscal', models.CharField(blank=True, max_length=5)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='GaContabilidad',
            fields=[
                ('idTipo', models.AutoField(primary_key=True, serialize=False)),
                ('GaContabilidad', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GaProyecto',
            fields=[
                ('idTipo', models.AutoField(primary_key=True, serialize=False)),
                ('GaProyecto', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Impuestos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TotalImpuestosTrasladados', models.CharField(blank=True, max_length=20)),
                ('TotalImpuestosRetenidos', models.CharField(blank=True, max_length=20)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='InContabilidad',
            fields=[
                ('idTipo', models.AutoField(primary_key=True, serialize=False)),
                ('InContabilidad', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InProyecto',
            fields=[
                ('idTipo', models.AutoField(primary_key=True, serialize=False)),
                ('InProyecto', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceEmitidas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Verificado_ó_Asoc', models.CharField(blank=True, max_length=150)),
                ('Estado_SAT', models.CharField(blank=True, max_length=150)),
                ('Version', models.CharField(blank=True, max_length=150)),
                ('Tipo', models.CharField(blank=True, max_length=150)),
                ('Fecha_Emision', models.CharField(blank=True, max_length=150)),
                ('Fecha_Timbrado', models.CharField(blank=True, max_length=150)),
                ('EstadoPago', models.CharField(blank=True, max_length=150)),
                ('FechaPago', models.CharField(blank=True, max_length=150)),
                ('Serie', models.CharField(blank=True, max_length=150)),
                ('Folio', models.CharField(blank=True, max_length=150)),
                ('UUID', models.CharField(blank=True, max_length=150)),
                ('UUID_Relacion', models.CharField(blank=True, max_length=150)),
                ('RFC_Emisor', models.CharField(blank=True, max_length=150)),
                ('Nombre_Emisor', models.CharField(blank=True, max_length=150)),
                ('LugarDeExpedicion', models.CharField(blank=True, max_length=150)),
                ('RFC_Receptor', models.CharField(blank=True, max_length=150)),
                ('Nombre_Receptor', models.CharField(blank=True, max_length=150)),
                ('ResidenciaFiscal', models.CharField(blank=True, max_length=150)),
                ('NumRegIdTrib', models.CharField(blank=True, max_length=150)),
                ('UsoCFDI', models.CharField(blank=True, max_length=150)),
                ('SubTotal', models.CharField(blank=True, max_length=150)),
                ('Descuento', models.CharField(blank=True, max_length=150)),
                ('Total_IEPS', models.CharField(blank=True, max_length=150)),
                ('IVA_16', models.CharField(blank=True, max_length=150)),
                ('Retenido_IVA', models.CharField(blank=True, max_length=150)),
                ('Retenido_ISR', models.CharField(blank=True, max_length=150)),
                ('ISH', models.CharField(blank=True, max_length=150)),
                ('Total', models.CharField(blank=True, max_length=150)),
                ('TotalOriginal', models.CharField(blank=True, max_length=150)),
                ('Total_Trasladados', models.CharField(blank=True, max_length=150)),
                ('Total_Retenidos', models.CharField(blank=True, max_length=150)),
                ('Total_LocalTrasladado', models.CharField(blank=True, max_length=150)),
                ('Total_LocalRetenido', models.CharField(blank=True, max_length=150)),
                ('Complemento', models.CharField(blank=True, max_length=150)),
                ('Moneda', models.CharField(blank=True, max_length=150)),
                ('Tipo_De_Cambio', models.CharField(blank=True, max_length=150)),
                ('Forma_De_Pago', models.CharField(blank=True, max_length=150)),
                ('Metodo_de_Pago', models.CharField(blank=True, max_length=150)),
                ('NumCtaPago', models.CharField(blank=True, max_length=150)),
                ('Condicion_de_Pago', models.CharField(blank=True, max_length=150)),
                ('Conceptos', models.CharField(blank=True, max_length=150)),
                ('Combustible', models.CharField(blank=True, max_length=150)),
                ('IEPS_3', models.CharField(blank=True, max_length=150)),
                ('IEPS_6', models.CharField(blank=True, max_length=150)),
                ('IEPS_7', models.CharField(blank=True, max_length=150)),
                ('IEPS_8', models.CharField(blank=True, max_length=150)),
                ('IEPS_9', models.CharField(blank=True, max_length=150)),
                ('IEPS_265', models.CharField(blank=True, max_length=150)),
                ('IEPS_30', models.CharField(blank=True, max_length=150)),
                ('IEPS_53', models.CharField(blank=True, max_length=150)),
                ('IEPS_160', models.CharField(blank=True, max_length=150)),
                ('Archivo_XML', models.CharField(blank=True, max_length=150)),
                ('Direccion_Emisor', models.CharField(blank=True, max_length=150)),
                ('Localidad_Emisor', models.CharField(blank=True, max_length=150)),
                ('Direccion_Receptor', models.CharField(blank=True, max_length=150)),
                ('Localidad_Receptor', models.CharField(blank=True, max_length=150)),
                ('IVA_8', models.CharField(blank=True, max_length=150)),
                ('IEPS_304', models.CharField(blank=True, max_length=150)),
                ('IVA_Ret_6', models.CharField(blank=True, max_length=150)),
                ('AÑO_Facturado', models.CharField(blank=True, max_length=150)),
                ('Mes_Facturado', models.CharField(blank=True, max_length=150)),
                ('Proyecto', models.CharField(blank=True, max_length=150)),
                ('Evento', models.CharField(blank=True, max_length=150)),
                ('SOCIO_EVENTO', models.CharField(blank=True, max_length=150)),
                ('NOMBRE_EVENTO', models.CharField(blank=True, max_length=150)),
                ('Forma_Cobro', models.CharField(blank=True, max_length=150)),
                ('ASOCIADOS_NO_ASOCIADOS', models.CharField(blank=True, max_length=150)),
                ('Año_cobro', models.CharField(blank=True, max_length=150)),
                ('Mes_Cobro', models.CharField(blank=True, max_length=150)),
                ('NOTAS', models.CharField(blank=True, max_length=150)),
                ('FOLIO_2', models.CharField(blank=True, max_length=150)),
                ('COMPLEMENTO_DE_PAGO', models.CharField(blank=True, max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Ultima Actualización')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceRecibidas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Verificado_ó_Asoc', models.CharField(blank=True, max_length=150)),
                ('Estado_SAT', models.CharField(blank=True, max_length=150)),
                ('Version', models.CharField(blank=True, max_length=150)),
                ('Tipo', models.CharField(blank=True, max_length=150)),
                ('Fecha_Emision', models.CharField(blank=True, max_length=150)),
                ('Fecha_Timbrado', models.CharField(blank=True, max_length=150)),
                ('EstadoPago', models.CharField(blank=True, max_length=150)),
                ('FechaPago', models.CharField(blank=True, max_length=150)),
                ('Serie', models.CharField(blank=True, max_length=150)),
                ('Folio', models.CharField(blank=True, max_length=150)),
                ('UUID', models.CharField(blank=True, max_length=150)),
                ('UUID_Relacion', models.CharField(blank=True, max_length=150)),
                ('RFC_Emisor', models.CharField(blank=True, max_length=150)),
                ('Nombre_Emisor', models.CharField(blank=True, max_length=150)),
                ('LugarDeExpedicion', models.CharField(blank=True, max_length=150)),
                ('RFC_Receptor', models.CharField(blank=True, max_length=150)),
                ('Nombre_Receptor', models.CharField(blank=True, max_length=150)),
                ('ResidenciaFiscal', models.CharField(blank=True, max_length=150)),
                ('NumRegIdTrib', models.CharField(blank=True, max_length=150)),
                ('UsoCFDI', models.CharField(blank=True, max_length=150)),
                ('SubTotal', models.CharField(blank=True, max_length=150)),
                ('Descuento', models.CharField(blank=True, max_length=150)),
                ('Total_IEPS', models.CharField(blank=True, max_length=150)),
                ('IVA_16', models.CharField(blank=True, max_length=150)),
                ('Retenido_IVA', models.CharField(blank=True, max_length=150)),
                ('Retenido_ISR', models.CharField(blank=True, max_length=150)),
                ('ISH', models.CharField(blank=True, max_length=150)),
                ('Total', models.CharField(blank=True, max_length=150)),
                ('TotalOriginal', models.CharField(blank=True, max_length=150)),
                ('TotalTrasladados', models.CharField(blank=True, max_length=150)),
                ('Total_Retenidos', models.CharField(blank=True, max_length=150)),
                ('Total_LocalTrasladado', models.CharField(blank=True, max_length=150)),
                ('Total_LocalRetenido', models.CharField(blank=True, max_length=150)),
                ('Complemento', models.CharField(blank=True, max_length=150)),
                ('Moneda', models.CharField(blank=True, max_length=150)),
                ('Tipo_De_Cambio', models.CharField(blank=True, max_length=150)),
                ('FormaDePago', models.CharField(blank=True, max_length=150)),
                ('Metodo_de_Pago', models.CharField(blank=True, max_length=150)),
                ('NumCtaPago', models.CharField(blank=True, max_length=150)),
                ('Condicion_de_Pago', models.CharField(blank=True, max_length=150)),
                ('Conceptos', models.CharField(blank=True, max_length=150)),
                ('Combustible', models.CharField(blank=True, max_length=150)),
                ('IEPS_3', models.CharField(blank=True, max_length=150)),
                ('IEPS_6', models.CharField(blank=True, max_length=150)),
                ('IEPS_7', models.CharField(blank=True, max_length=150)),
                ('IEPS_8', models.CharField(blank=True, max_length=150)),
                ('IEPS_9', models.CharField(blank=True, max_length=150)),
                ('IEPS_265', models.CharField(blank=True, max_length=150)),
                ('IEPS_30', models.CharField(blank=True, max_length=150)),
                ('IEPS_53', models.CharField(blank=True, max_length=150)),
                ('IEPS_160', models.CharField(blank=True, max_length=150)),
                ('Archivo_XML', models.CharField(blank=True, max_length=150)),
                ('Direccion_Emisor', models.CharField(blank=True, max_length=150)),
                ('Localidad_Emisor', models.CharField(blank=True, max_length=150)),
                ('Direccion_Receptor', models.CharField(blank=True, max_length=150)),
                ('Localidad_Receptor', models.CharField(blank=True, max_length=150)),
                ('IVA_8', models.CharField(blank=True, max_length=150)),
                ('IEPS_304', models.CharField(blank=True, max_length=150)),
                ('IVA_Ret_6', models.CharField(blank=True, max_length=150)),
                ('AÑO', models.CharField(blank=True, max_length=150)),
                ('MES_FACTURADO', models.CharField(blank=True, max_length=150)),
                ('PROYECTO', models.CharField(blank=True, max_length=150)),
                ('CONTABILIDAD', models.CharField(blank=True, max_length=150)),
                ('ESTATUS_PAGO', models.CharField(blank=True, max_length=150)),
                ('BANCO', models.CharField(blank=True, max_length=150)),
                ('Mes_Pago_BANCO', models.CharField(blank=True, max_length=150)),
                ('AÑO_PAGO_BANCO', models.CharField(blank=True, max_length=150)),
                ('NOTAS', models.CharField(blank=True, max_length=150)),
                ('TIPO_IVA', models.CharField(blank=True, max_length=150)),
                ('DIOT_COEFICIENTE', models.CharField(blank=True, max_length=150)),
                ('DIOT_BASE_16', models.CharField(blank=True, max_length=150)),
                ('DIOT_IVA', models.CharField(blank=True, max_length=150)),
                ('COMPLEMENTO_DE_PAGO', models.CharField(blank=True, max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Ultima Actualización')),
            ],
        ),
        migrations.CreateModel(
            name='NEmisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RegistroPatronal', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Nomina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaFinalPago', models.CharField(blank=True, max_length=50)),
                ('FechaInicialPago', models.CharField(blank=True, max_length=50)),
                ('FechaPago', models.CharField(blank=True, max_length=50)),
                ('NumDiasPagados', models.CharField(blank=True, max_length=50)),
                ('TipoNomina', models.CharField(blank=True, max_length=50)),
                ('TotalOtrosPagos', models.CharField(blank=True, max_length=50)),
                ('TotalPercepciones', models.CharField(blank=True, max_length=50)),
                ('Version', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='NPercepcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Clave', models.CharField(blank=True, max_length=50)),
                ('Concepto', models.CharField(blank=True, max_length=50)),
                ('ImporteExento', models.CharField(blank=True, max_length=50)),
                ('ImporteGravado', models.CharField(blank=True, max_length=50)),
                ('TipoPercepcion', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='NPercepciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TotalExento', models.CharField(blank=True, max_length=50)),
                ('TotalGravado', models.CharField(blank=True, max_length=50)),
                ('TotalSueldos', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='NReceptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Antigüedad', models.CharField(blank=True, max_length=50)),
                ('ClaveEntFed', models.CharField(blank=True, max_length=50)),
                ('Curp', models.CharField(blank=True, max_length=50)),
                ('Departamento', models.CharField(blank=True, max_length=50)),
                ('FechaInicioRelLaboral', models.CharField(blank=True, max_length=50)),
                ('NumEmpleado', models.CharField(blank=True, max_length=50)),
                ('NumSeguridadSocial', models.CharField(blank=True, max_length=50)),
                ('PeriodicidadPago', models.CharField(blank=True, max_length=50)),
                ('Puesto', models.CharField(blank=True, max_length=50)),
                ('RiesgoPuesto', models.CharField(blank=True, max_length=50)),
                ('SalarioBaseCotApor', models.CharField(blank=True, max_length=50)),
                ('SalarioDiarioIntegrado', models.CharField(blank=True, max_length=50)),
                ('Sindicalizado', models.CharField(blank=True, max_length=50)),
                ('TipoContrato', models.CharField(blank=True, max_length=50)),
                ('TipoJornada', models.CharField(blank=True, max_length=50)),
                ('TipoRegimen', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='OtroPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Clave', models.CharField(blank=True, max_length=50)),
                ('Concepto', models.CharField(blank=True, max_length=50)),
                ('Importe', models.CharField(blank=True, max_length=50)),
                ('TipoOtroPago', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaPago', models.CharField(blank=True, max_length=20)),
                ('FormaDePagoP', models.CharField(blank=True, max_length=20)),
                ('MonedaP', models.CharField(blank=True, max_length=20)),
                ('Monto', models.CharField(blank=True, max_length=20)),
                ('NumOperacion', models.CharField(blank=True, max_length=150)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Receptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rfc', models.CharField(blank=True, max_length=15)),
                ('Nombre', models.CharField(blank=True, max_length=250)),
                ('UsoCFDI', models.CharField(blank=True, max_length=5)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='SubsidioAlEmpleo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SubsidioCausado', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='TimbreFiscalDigital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Version', models.CharField(blank=True, max_length=5)),
                ('UUID', models.CharField(blank=True, max_length=150)),
                ('FechaTimbrado', models.CharField(blank=True, max_length=30)),
                ('RfcProvCertif', models.CharField(blank=True, max_length=20)),
                ('NoCertificadoSAT', models.CharField(blank=True, max_length=20)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Traslado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Base', models.CharField(blank=True, max_length=20)),
                ('Impuesto', models.CharField(blank=True, max_length=20)),
                ('TipoFactor', models.CharField(blank=True, max_length=20)),
                ('TasaOCuota', models.CharField(blank=True, max_length=20)),
                ('Importe', models.CharField(blank=True, max_length=20)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='DatosFactura',
            fields=[
                ('idDato', models.AutoField(default='', editable=False, primary_key=True, serialize=False, verbose_name='DatosFactura')),
                ('InContabilidad', models.CharField(blank=True, max_length=50)),
                ('GaProyecto', models.CharField(blank=True, max_length=50)),
                ('GaContabilidad', models.CharField(blank=True, max_length=50)),
                ('UUIDInt', models.CharField(blank=True, max_length=60)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('InProyecto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='conciliacion.inproyecto', verbose_name='Ingreso proyecto')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
