from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.db.models.functions import Substr
from django.db.models import Sum
from django.db import connection
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import String
from openpyxl import Workbook

import environ, sys


# Create your views here.

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                do_login(request, user)
                return redirect("/menu")
    return render(request, "login.html")


def logout(request):
    do_logout(request)
    return redirect("/")


def menu(request):

    titulo = "Olvera Contadores & Asesores"

    context = {
        "titulo": titulo,
    }

    return render(request, "menu.html", context)


def invoice(request):

    frmNombre = request.POST.get("Cliente", "")
    frmRFC = request.POST.get("RFC", "")
    frmAño = request.POST.get("Anio", "")
    frmMes = request.POST.get("Mes", "")
    frmTrue = request.POST.get("frmEnvia", "")

    titulo = "Reporte de facturas emitidas"

    if request.POST.get("frmEnvia", "") == "":
        NombreFiltro = ""
        RFCFiltro = ""
        AñoFiltro = ""
        MesFiltro = ""
    else:
        limit = ""
        RFCFiltro = "and Rfc like CONCAT(char(37), '" + frmRFC + "' ,Char(37)) "
        NombreFiltro = (
            "and Nombre like CONCAT(char(37), '" + frmNombre + "' ,Char(37)) "
        )
        AñoFiltro = "and YEAR(Fecha) like CONCAT(char(37), '" + frmAño + "' ,Char(37)) "
        MesFiltro = (
            "and DATE_FORMAT(Fecha, CONCAT(char(37), 'm')) like CONCAT(char(37), '"
            + frmMes
            + "' ,Char(37)) "
        )

    queryset = Comprobante.objects.raw(
        "select 1 as id, upper(b.Nombre) Nombre, a.SubTotal, ROUND(a.Total-a.SubTotal, 2) IVA, Total, c.Descripcion, d.TasaOCuota*100 TasaOCuota, d.Importe, b.Rfc, "
        "Moneda, a.UUIDInt, YEAR(Fecha) Periodo, DATE_FORMAT(Fecha, CONCAT(char(37), 'm')) Mes "
        "from conciliacion_comprobante a "
        "inner join conciliacion_receptor b "
        "on a.IDKey = b.IDKey "
        "inner join conciliacion_concepto c "
        "on a.IDKey = c.IDKey "
        "left join conciliacion_traslado d "
        "on a.IDKey = d.IDKey "
        "where a.TipoEmRe = 'Emitidas' "
        + RFCFiltro
        + NombreFiltro
        + AñoFiltro
        + MesFiltro
        + " group by a.UUIDInt "
        + "order by Fecha desc, Nombre "
    )

    print(queryset)

    paginator = Paginator(queryset, 15)
    page = request.GET.get("page")

    rfc = Emisor.objects.raw(
        "select distinct 1 as id, Rfc from conciliacion_receptor order by 2"
    )
    # print(rfc)
    anio = Comprobante.objects.raw(
        "select distinct 1 as id, year(Fecha) Año from conciliacion_comprobante order by 2"
    )
    mes = Comprobante.objects.raw(
        'select distinct 1 as id, DATE_FORMAT(Fecha, CONCAT(char(37), "m")) Mes from conciliacion_comprobante order by cast(month(Fecha) as int)'
    )

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    context = {
        "titulo": titulo,
        "qry": queryset,
        "rfc": rfc,
        "anio": anio,
        "mes": mes,
        "NombreFiltro": "Nombre: " + frmNombre,
        "RFCFiltro": "RFC: " + frmRFC,
        "AñoFiltro": "Año: " + frmAño,
        "MesFiltro": "Mes: " + frmMes,
        "frmTrue": frmTrue,
        "items": items,
    }

    return render(request, "importar.html", context)


def invoiceDetail(request, Rfc, Periodo, Mes, Moneda):

    # print("RFC: " + Rfc)
    # print("Periodo: " + Periodo)
    # print("Mes: " + Mes)
    # print("Moneda: " + Moneda)

    titulo = "Detalle de facturas"
    query = Comprobante.objects.raw(
        "select 1 as id, Version, Serie, Folio, Fecha, SubTotal, Total, MetodoPago, Moneda, SUBSTRING_INDEX(b.UUIDInt, '@', 1) UUIDInt, c.idDato from conciliacion_comprobante a "
        "inner join conciliacion_emisor b "
        "on a.UUIDInt = b.UUIDInt "
        "left join conciliacion_datosfactura c on SUBSTRING_INDEX(a.UUIDInt, '@', 1) = SUBSTRING_INDEX(c.UUIDInt, '@', 1) "
        "where Rfc = '" + Rfc + "' "
        "and YEAR(Fecha) = '" + Periodo + "' "
        "and DATE_FORMAT(Fecha, CONCAT(char(37), 'm')) = '" + Mes + "' "
        "and Moneda = '" + Moneda + "'"
    )
    # print(query)

    context = {
        "titulo": titulo,
        "query": query,
        "RFC": Rfc,
        "Periodo": Periodo,
        "Mes": Mes,
        "Moneda": Moneda,
    }

    return render(request, "detailInvoice.html", context)


def detailFact(request, UUIDInt):

    form = addDatos(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            print("Si entra")
            frm = form.save(commit=False)
            # idUsuario = form.cleaned_data.get("idUsuario")
            # InProyecto = form.cleaned_data.get("InProyecto")
            # InContabilidad = form.cleaned_data.get("InContabilidad")
            # GaProyecto = form.cleaned_data.get("GaProyecto")
            # GaContabilidad = form.cleaned_data.get("GaContabilidad")
            # UUIDInt = form.cleaned_data.get("UUIDInt")
            # print(UUIDInt)
            frm.save()

            # return redirect('/invoiceDetail/' + qRFC + '/' + Periodo + '/' + Mes + '/' + Moneda)

    context = {
        "Titulo": "Agregar datos adicionales ",
        "UUID": UUIDInt,
        "form": form,
    }

    return render(request, "modal.html", context)


def parcialidades(request):

    qry = Comprobante.objects.raw(
        "select 1 as id, tbl.*, b.UUIDInt, b.Total,  YEAR(b.Fecha) Año, MONTH(b.Fecha) Mes from ("
        "select count(1) NoParc, IdDocumento, Sum(ImpPagado) ImpPagado, Sum(ImpSaldoAnt) ImpSaldoAnt, Sum(ImpSaldoInsoluto) ImpSaldoInsoluto "
        "from conciliacion_doctorelacionado group by IdDocumento "
        ") tbl "
        "inner join conciliacion_comprobante b "
        "on SUBSTRING_INDEX(b.UUIDInt, '@', 1) = tbl.IdDocumento"
    )

    context = {
        "Titulo": "Parcialidades",
        "qry": qry,
    }

    return render(request, "reporteParcialidad.html", context)


def receipts(request):

    titulo = "Importar reporte de facturas recibidas"

    queryset = Comprobante.objects.raw(
        "select 1 as id, upper(b.Nombre) Nombre, a.SubTotal, ROUND(a.Total-a.SubTotal, 2) IVA, Total, c.Descripcion, d.TasaOCuota*100 TasaOCuota, d.Importe, b.Rfc, "
        "Moneda, a.UUIDInt, YEAR(Fecha) Periodo, DATE_FORMAT(Fecha, CONCAT(char(37), 'm')) Mes "
        "from conciliacion_comprobante a "
        "inner join conciliacion_receptor b "
        "on a.IDKey = b.IDKey "
        "inner join conciliacion_concepto c "
        "on a.IDKey = c.IDKey "
        "left join conciliacion_traslado d "
        "on a.IDKey = d.IDKey "
        "where a.TipoEmRe = 'Recibidas' "
        "group by a.UUIDInt order by Fecha desc, Nombre "
    )

    print(queryset)

    context = {"titulo": titulo, "qry": queryset}

    return render(request, "recibidas.html", context)


def customers(request):
    titulo = "Clientes"
    user = request.user

    # queryset = Invoice.objects.all().order_by('Nombre_Receptor').filter(Nombre_Receptor='Carlos Enrique Ortega Mora')

    queryset = (
        InvoiceEmitidas.objects.values("RFC_Receptor", "Moneda")
        .order_by("RFC_Receptor")
        .annotate(total_price=Sum("Total"))
    )  # .filter(Nombre_Receptor='Carlos Enrique Ortega Mora')

    # print(queryset.query)

    context = {
        "titulo": titulo,
        "usr": user,
        "qry": queryset,
    }

    return render(request, "clientes.html", context)


def repEmitidas(request):
    titulo = "Reporte Facturas Emitidas"

    queryset = InvoiceEmitidas.objects.raw(
        """select id, Mes, Año, sum(SubTotal) SubTotal, sum(IVA_16) IVA_16, sum(Total) Total  from (
                                    select id, Fecha_Emision, SubTotal, IVA_16, Total, SUBSTR(Fecha_Emision, 4, 2) Mes, SUBSTR(Fecha_Emision, 7, 4) Año, timestamp 
                                    from conciliacion_invoiceemitidas                                    
                                    ) tbl
                                    group by Mes, Año
                                    order by 3, 2"""
    )
    """
    queryset = Invoice.objects.values('Fecha_Emision', 'IVA_16', 'Total'
            ).annotate(Sub_Total=Sum('SubTotal')
                       )
                       """
    # print(queryset.query)

    context = {"titulo": titulo, "qry": queryset}
    return render(request, "emitidas.html", context)


def repRecibidas(request):
    titulo = "Reporte Facturas Recibidas"

    queryset = InvoiceRecibidas.objects.raw(
        """select id, Mes, Año, sum(SubTotal) SubTotal, Sum(IVA_16) IVA_16, 
                                    Sum(Retenido_IVA) Retenido_IVA, Sum(Retenido_ISR) Retenido_ISR, Sum(Total) Total from 
                                    (select id, Fecha_Emision, SUBSTR(Fecha_Emision, 4,2) Mes, SUBSTR(Fecha_Emision, 7, 4) Año, 
                                    SubTotal, IVA_16, Retenido_IVA, Retenido_ISR, Total from conciliacion_invoicerecibidas
                                    ) tbl
                                    where Total > 0
                                    group by Mes, Año
                                    Order by 3, 2"""
    )

    context = {"titulo": titulo, "qry": queryset}

    return render(request, "factRecibidas.html", context)


def importBalanza(mes, new_conciliacion, txt):

    fname = new_conciliacion
    print("Nombre archivo " + str(fname))
    stream = fname.read()
    e = ""

    try:
        df = pd.read_excel(stream, sheet_name=mes)
        print(df)

        engine = create_engine(env("conn"))
        df.to_sql("conciliacion_balance", con=engine, if_exists="append", index=False)

    except Exception:
        e = sys.exc_info()
        txt = "Hubo un error al subir el archivo, favor de comunicarse con el administrador"
        print(txt)
        print(e)

    finally:
        hideForm = 1
        file = txt

        return txt, e


def impConciliacion(request):

    titulo = "Importar balanza de comprobación"
    file = ""
    txt = "El archivo subió correctamente"
    hideForm = 0
    e = ""

    if request.method == "POST":

        new_conciliacion = request.FILES["xlsfile"]

        r = request.POST.get("all", "")
        print(r)

        if request.POST.get("all", "") == "":

            print("Entro a solo un mes")
            mes = request.POST.get("mes", "")

            print("Este es el mes que yo quiero importar: " + mes)

            importBalanza(mes, new_conciliacion, txt)

        else:

            print("ahora importara los 12 meses")
            fname = new_conciliacion
            print("Nombre archivo " + str(fname))
            stream = fname.read()

            # if not os.path.isfile(new_conciliacion):
            #    print("ya valio")
            #    return None

            xls = pd.read_excel(stream, None)
            # xls = pd.ExcelFile(stream)
            t = xls.keys()
            print(t)
            # print(xls)
            # sheets = xls.sheet_names
            # results = {}

            for sheet in t:
                # results[sheet] = xls.parse(sheet)
                print("Importando mes: " + sheet)
                # print(results[sheet])

                try:
                    # stream = fname.read()
                    df = pd.read_excel(stream, sheet_name=sheet)
                    print(df)
                    engine = create_engine(env("conn"))
                    df.to_sql(
                        "conciliacion_balance",
                        con=engine,
                        if_exists="append",
                        index=False,
                    )

                except Exception:
                    e = sys.exc_info()
                    txt = "Hubo un error al subir el archivo, favor de comunicarse con el administrador"
                    print(txt)
                    print(e)

                finally:
                    hideForm = 1
                    file = txt

        hideForm = 1
        file = txt

    context = {
        "titulo": titulo,
        "file": file,
        "hideForm": hideForm,
        "error": e,
    }

    return render(request, "importBalanza.html", context)


def conciliacion(request):

    titulo = "Conciliación"

    rfc = Balance.objects.values("RFC").distinct()

    cuenta = request.GET.get("cuenta", "")
    campo_1 = request.GET.get("campo_1", "")
    campo_2 = request.GET.get("campo_2", "")
    tabla = request.GET.get("tabla", "")
    title_1 = request.GET.get("title_1", "")
    title_2 = request.GET.get("title_2", "")
    RFC = request.GET.get("RFC", "")

    print(cuenta)

    if request.method == "GET":

        try:

            r105 = InvoiceEmitidas.objects.raw(
                """select id, Cuenta, Mes, Año, Sum("""
                + campo_1
                + """) campo_1, """
                + campo_2
                + """ campo_2, (Sum("""
                + campo_1
                + """) - """
                + campo_2
                + """) Diff, TipoEmRe from (select a.id, b.Cuenta, DATE_FORMAT(Fecha, CONCAT(char(37), 'm')) Mes, 
                YEAR(a.Fecha) Año, a."""
                + campo_1
                + """, b."""
                + campo_2
                + """, b.Rfc, a.TipoEmRe from """
                + tabla
                + """ a inner join conciliacion_balance b
                    on YEAR(a.Fecha) and b.Año 
                    and MONTH(a.Fecha) = b.Mes
                    inner join conciliacion_emisor c
                    on a.IDKey = c.IDKey 
                    and c.Rfc = b.Rfc
                    and b.Rfc = '"""
                + RFC
                + """'                                    
                                        where Cuenta like CONCAT('"""
                + cuenta
                + """', char(37))
                                        ) tbl
                                        group by Mes, Año, """
                + campo_2
                + ", Cuenta, Rfc, TipoEmRe"
            )
            print(r105)

        except Exception():
            print(r105)

        context = {
            "titulo": titulo,
            "r105": r105,
            "title_1": title_1,
            "title_2": title_2,
            "cuenta": cuenta,
            "rfc": rfc,
        }
    # print(r105)
    # print(rfc)

    return render(request, "conciliacion.html", context)


def impbalanza(request):

    titulo = "Archivos cargados"

    balanzas = Balance.objects.values("RFC", "Mes", "Año", "timestamp").distinct()
    emitidas = InvoiceEmitidas.objects.raw(
        "select DISTINCT 1 id, timestamp, RFC_Emisor, replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') fecha, count(1) Total from conciliacion_invoiceemitidas group by timestamp, RFC_Emisor"
    )
    recibidas = InvoiceRecibidas.objects.raw(
        "select DISTINCT 1 id, timestamp, RFC_Receptor, replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') fecha, count(1) Total from conciliacion_invoicerecibidas group by timestamp, RFC_Receptor"
    )
    print(emitidas)
    print(recibidas)

    context = {
        "titulo": titulo,
        "balanzas": balanzas,
        "emitidas": emitidas,
        "recibidas": recibidas,
    }

    return render(request, "balanzasCargadas.html", context)


def delete_balanza(request, balanza_id):

    delete = str(balanza_id)

    try:
        # selBalanza = Balance.objects.get(Concat(Mes, Año) = delete)
        # selBalanza = Balance.objects.raw("delete from conciliacion_balance where CONCAT(Mes, Año) = '" + delete + "'")
        # print(selBalanza)

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM conciliacion_balance WHERE CONCAT(Mes, Año, RFC) = '"
                + delete
                + "'"
            )
        # "DELETE FROM mydb_mymodel WHERE s_type = '%s' AND barcode = '%s' AND shopcode = '%s' AND date = '%s'" ,
        # [d.s_type,d.barcode,d.shopcode,d.date]
    # )
    except Balance.DoesNotExist:
        # print('No jalo :(')
        return redirect("menu")

    # selBalanza.delete()

    return redirect("impbalanza")


def delete_factemitidas(request, factemitidas_id):

    factura = str(factemitidas_id)

    try:
        with connection.cursor() as cursor:
            # cursor = "select DISTINCT timestamp from conciliacion_invoiceemitidas where replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') = '" + factura + "'"
            cursor.execute(
                "delete from conciliacion_invoiceemitidas where replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') = '"
                + factura
                + "'"
            )
            print(cursor)

    except InvoiceEmitidas.DoesNotExist:
        # print('No jalo :(')
        return redirect("menu")

    finally:
        print("Eliminación de facturas emitidas con fecha: " + factura)

    return redirect("impbalanza")


def delete_factrecibidas(request, factrecibidas_id):

    factura = str(factrecibidas_id)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "delete from conciliacion_invoicerecibidas where replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') = '"
                + factura
                + "'"
            )
            print(cursor)

    except InvoiceRecibidas.DoesNotExist:
        # print('No jalo :(')
        return redirect("menu")

    finally:
        print("Eliminación de facturas emitidas con fecha: " + factura)

    return redirect("impbalanza")


def pagoprov(request):

    # form = RFC(request.POST or None)

    RFC = request.POST.get("RFC_Emisor", "")
    # RFC_comp = "'" + RFC + "'"

    dsISR_SP = InvoiceEmitidas.objects.raw(
        """select 1 as id, SUBSTR(Fecha_Emision, 4, 2) Mes, 
                              RFC_Emisor, round(sum(IVA_16)) IVA_16, round(sum(IVA_16)/0.16) SP_16, round(Sum(Total)) Total
                              from conciliacion_invoiceemitidas 
                              where SUBSTR(Fecha_Emision, 7, 4) = 2020                               
                              and RFC_Emisor =  '"""
        + RFC
        + """'
                              and PROYECTO = 'Supervisión de Proyectos'
                              and Tipo = 'Factura'                              
                              group by RFC_Emisor, SUBSTR(Fecha_Emision, 4, 2)
                              order by RFC_Emisor ASC"""
    )

    dsISR_TR = InvoiceEmitidas.objects.raw(
        """select 1 as id, SUBSTR(Fecha_Emision, 4, 2) Mes, 
                              RFC_Emisor, round(sum(IVA_16)) IVA_16, round(sum(IVA_16)/0.16) TR_16, round(Sum(Total)) Total
                              from conciliacion_invoiceemitidas 
                              where SUBSTR(Fecha_Emision, 7, 4) = 2020                               
                              and RFC_Emisor =  '"""
        + RFC
        + """'
                              and PROYECTO = 'Transporte'
                              and Tipo = 'Factura'                              
                              group by RFC_Emisor, SUBSTR(Fecha_Emision, 4, 2)
                              order by RFC_Emisor ASC"""
    )

    dsISR_IN = InvoiceEmitidas.objects.raw(
        """select 1 as id, SUBSTR(Fecha_Emision, 4, 2) Mes, 
                              RFC_Emisor, round(sum(IVA_16)) IVA_16, round(sum(IVA_16)/0.16) SP_16, round(Sum(Total)) Total
                              from conciliacion_invoiceemitidas 
                              where SUBSTR(Fecha_Emision, 7, 4) = 2020                               
                              and RFC_Emisor =  '"""
        + RFC
        + """'
                              and PROYECTO = 'Supervisión de Proyectos'
                              and Tipo = 'Factura'                              
                              group by RFC_Emisor, SUBSTR(Fecha_Emision, 4, 2)
                              order by RFC_Emisor ASC"""
    )

    """
    x = InvoiceEmitidas.objects.values('Fecha_Emision', 'RFC_Emisor'
                               ).order_by('Fecha_Emision'
                                          ).annotate(IVA_16=Sum('IVA_16'), SP_16=Sum('IVA_16')/0.16
                                                     ).filter(RFC_Emisor=RFC_comp)                                  
   
    print(x.query)
    
    y = x.filter(Proyecto__startswith="Supervi")
    
    print(y.query)
    """

    context = {
        "qryISR": dsISR_SP,
        "qryISR_TR": dsISR_TR,
        "qryISR_IN": dsISR_IN
        # "frm" : form
    }

    return render(request, "pagoProv.html", context)


class BasicListView(View):
    model = None

    def get(self, request, *args, **kwargs):
        objects = self.model.objects.raw(
            """select 1 as id, SUBSTR(Fecha_Emision, 4, 2) Mes, RFC_Emisor, round(sum(IVA_16)) IVA_16, round(sum(IVA_16)/0.16) SP_16, round(Sum(Total)) Total
                              from conciliacion_invoiceemitidas 
                              where SUBSTR(Fecha_Emision, 7, 4) = 2020                               
                              and RFC_Emisor = 'SUFF690719CI8' 
                              and PROYECTO = 'Supervisión de Proyectos'
                              and Tipo = 'Factura'                              
                              group by RFC_Emisor, SUBSTR(Fecha_Emision, 4, 2)
                              order by RFC_Emisor ASC"""
        )
        context = {
            "qry": objects,
        }

        print(objects.query)

        return render(request, "pagoProv.html", context)


# View to display a list of countries
class ISR_Em(BasicListView):
    model = Balance


def export_data(request, cuenta, campo_1, campo_2, tabla, title_1, title_2):
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="Conciliacion.xlsx"'

    # create workbook
    wb = Workbook()
    sheet = wb.active

    # export data to Excel
    # rows = .objects.all().values_list('')
    rows = InvoiceEmitidas.objects.raw(
        """select id, Cuenta, Mes, Año, Sum("""
        + campo_1
        + """) campo_1, """
        + campo_2
        + """ campo_2, (Sum("""
        + campo_1
        + """) - """
        + campo_2
        + """) Diff from (
                                    select a.id, Cuenta, SUBSTR(a.Fecha_Emision, 4, 2) Mes, SUBSTR(a.Fecha_Emision, 7, 4) Año, a."""
        + campo_1
        + """, b."""
        + campo_2
        + """ 
                                    from """
        + tabla
        + """ a 
                                    inner join conciliacion_balance b
                                    on SUBSTR(a.Fecha_Emision, 4, 2) = case when LENGTH(b.Mes) = 1 then Concat('0', b.Mes) when LENGTH(b.Mes) = 2 then b.Mes end
                                    and SUBSTR(a.Fecha_Emision, 7, 4) = b.Año
                                    where Cuenta = '"""
        + cuenta
        + """'
                                    ) tbl
                                    group by Mes, Año, """
        + campo_2
        + """, Cuenta
                                    """
    )

    for row_num, row in enumerate(rows, 1):
        # row is just a tuple
        for col_num, value in enumerate(row):
            c5 = sheet.cell(row=row_num + 1, column=col_num + 1)
            c5.value = value

    wb.save(response)

    return response


def import_data(request):
    if request.method == "POST":
        file_format = request.POST["file-format"]
        employee_resource = EmployeeResource()
        dataset = Dataset()
        new_employees = request.FILES["importData"]

        if file_format == "CSV":
            imported_data = dataset.load(
                new_employees.read().decode("utf-8"), format="csv"
            )
            result = employee_resource.import_data(dataset, dry_run=True)
        elif file_format == "JSON":
            imported_data = dataset.load(
                new_employees.read().decode("utf-8"), format="json"
            )
            # Testing data import
            result = employee_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            # Import now
            employee_resource.import_data(dataset, dry_run=False)

    return render(request, "import.html")
