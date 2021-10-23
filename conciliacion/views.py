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
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/')
def menu(request):

    titulo = "Olvera Contadores & Asesores"

    context = {
        "titulo": titulo,
    }

    return render(request, "menu.html", context)

@login_required(login_url='/')
def invoice(request):

    frmNombre = request.POST.get("Cliente", "")
    frmRFC = request.POST.get("RFC", "")
    frmAño = request.POST.get("Anio", "")
    frmMes = request.POST.get("Mes", "")
    frmTrue = request.POST.get("frmEnvia", "")
    queryset = ""
    items = ""
    txtInicial = ""

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
        
        
    if request.POST.get("frmEnvia", "") == "":
        txtInicial = "Selecciona un filtro para mostrar las facturas"
    else:
        queryset = Comprobante.objects.raw("select 1 as id, upper(b.Nombre) Nombre, a.SubTotal, ROUND(a.Total-a.SubTotal, 2) IVA, Total, c.Descripcion, "
                                           "d.TasaOCuota*100 TasaOCuota, d.Importe, b.Rfc, a.TipoCambio, "
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
                                           + "order by Fecha desc, Nombre Limit 10"
                                           )
        print(queryset)
        
        paginator = Paginator(queryset, 15)
        page = request.GET.get("page")
        
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)

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
        "txt" : txtInicial,
    }

    return render(request, "importar.html", context)


def invoiceDetail(request, UUID):

    titulo = "Detalle de facturas"
    fact = "Facturas relacionadas"
    
    query = DoctoRelacionado.objects.raw("select * from conciliacion_doctorelacionado where IdDocumento = '" + UUID + "'")
    
    #query = DoctoRelacionado.objects.all()
    print(query)

    context = {
        "titulo": titulo,
        "query": query,       
        "rel" : fact, 
        "ID" : UUID,
    }

    return render(request, "detailInvoice.html", context)

def detailFact(request, UUIDInt):

    form = addDatos(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            print("Si entra")
            frm = form.save(commit=False)
            frm.save()
    
    context = {
        "Titulo": "Agregar datos adicionales ",
        "UUID": UUIDInt,
        "form": form,
    }

    return render(request, "modal.html", context)

@login_required(login_url='/')
def calcNomina(request):
    
    titulo = "Calculadora ISR Sueldos"
    monto = request.POST.get("monto", "")
    montoQ = request.POST.get("monto", "")
    mensual = ""
    list = ""
    #print(monto)    
    
    
    if(monto):
        
        mensual = TablaMensual.objects.raw("select 1 as id, Bruto, LI, Excedente, Tasa, (Excedente*Tasa) ImpMarginal, CuotaFija, "
                                           "(Excedente*Tasa)+CuotaFija as ISR, "
                                           "Subsidio, (((Excedente*Tasa)+CuotaFija)-Subsidio) ISRReten, (((Excedente*Tasa)+CuotaFija)-Subsidio)/2 ISRQuin, "
                                           + monto + "-(((Excedente*Tasa)+CuotaFija)-Subsidio) Neto, " 
                                           + monto + "/30 CuotaDiaria from ( "
                                           "select " + monto +" as Bruto, LimiteInferior LI, (" + monto +"-LimiteInferior) Excedente, "
                                           "(select PorcExcedente from conciliacion_tablamensual where LimiteInferior < " + monto + " and LimiteSuperior > " + monto + ") TASA, "
                                           "(select CuotaFija from conciliacion_tablamensual where LimiteInferior < " + monto + " and LimiteSuperior > " + monto + ") CuotaFija, "
                                           "(select SubsidioAlEmpleo from conciliacion_tablasubsidiom where LimiteInferior < " + monto + " and LimiteSuperior > " + monto + ") as Subsidio "
                                           "from conciliacion_tablamensual where LimiteInferior < " + monto + " and LimiteSuperior > " + monto + ") tbl")
    
        #print(mensual)
        
        quincenal = TablaQuincenal.objects.raw("select 1 as id, Bruto, LI, Excedente, Tasa, (Excedente*Tasa) ImpMarginal, CuotaFija, "
                                           "(Excedente*Tasa)+CuotaFija as ISR, "
                                           "Subsidio, (((Excedente*Tasa)+CuotaFija)-Subsidio) ISRReten, (((Excedente*Tasa)+CuotaFija)-Subsidio)/2 ISRQuin, "
                                           #+ montoQ + "-(((Excedente*Tasa)+CuotaFija)-Subsidio) Neto, " 
                                           "1500-(((Excedente*Tasa)+CuotaFija)-Subsidio) Neto, "
                                           + montoQ + "/30 CuotaDiaria from ( "
                                           "select " + montoQ +"/2 as Bruto, LimiteInferior LI, ((" + montoQ +"/2)-LimiteInferior) Excedente, "
                                           "(select PorcExcedente from conciliacion_tablaquincenal where LimiteInferior < " + montoQ + "/2 and LimiteSuperior > " + montoQ + "/2) TASA, "
                                           "(select CuotaFija from conciliacion_tablaquincenal where LimiteInferior < " + montoQ + "/2 and LimiteSuperior > " + montoQ + "/2) CuotaFija, "
                                           "(select SubsidioAlEmpleo from conciliacion_tablasubsidioq where LimiteInferior < " + montoQ + "/2 and LimiteSuperior > " + montoQ + "/2) as Subsidio "
                                           "from conciliacion_tablaquincenal where LimiteInferior < " + montoQ + "/2 and LimiteSuperior > " + montoQ + "/2) tbl")
        
        print(quincenal)
        
        list = zip(mensual, quincenal)
    
    context = {
        "title" : titulo,
        #"mensual" : mensual,
        "monto" : monto,
        #"quincenal" : quincenal,
        "nomina" : list,
    }
    
    return render(request, "calcNomina.html", context)

@login_required(login_url='/')
def calcIMSS(request):

    title = "Calculadora IMSS"
    factInt = ""
    monto = request.POST.get("monto", "")
    dias = request.POST.get("dias", "")
    frmTrue = request.POST.get("frmEnvia", "")    

    #datosPatron = DatosPatronIMSS.objects.all()

    if request.POST.get("frmEnvia", "") != "":
        
        #factInt = FactorIntegracion.objects.raw("select id, uma, DOF, FactIntg, uma3, case when DOF*FactIntg > (select uma*25 from conciliacion_uma) then "
        #                                    "(select uma*25 from conciliacion_uma) else DOF*FactIntg  end SDI from (select 1 as id, (select UMA from conciliacion_uma) uma, " + monto + "/30 DOF, "
        #                                    "((Aguinaldo/365)+((DVacaciones/365)*PVacacional))+Antiguedad FactIntg, (select UMA*3* " + dias + " from conciliacion_uma) uma3 "
        #                                    "from conciliacion_factorintegracion) tbl")

        factInt = FactorIntegracion.objects.raw("select *, cuotafija+ExcedentePatronal+PrestDineat+GMPP+InvalidezVP+Guarderias+ExcedenteObrero+PrestObrero+GMPO+RiesgosTrabajo+InvalidezVO TotalIMSS, "
                    "Retiro+CEAVObrero+CEAVP TotalRCV, "
                    "Retiro+CEAVObrero+CEAVP+acvpatronal TotalInfonavit, "
                    "(cuotafija+ExcedentePatronal+PrestDineat+GMPP+InvalidezVP+Guarderias+ExcedenteObrero+PrestObrero+GMPO+RiesgosTrabajo+InvalidezVO)+(Retiro+CEAVObrero+CEAVP+acvpatronal) CostoSegSoc, "
                    "(cuotafija+ExcedentePatronal+PrestDineat+GMPP+InvalidezVP+Guarderias+Retiro+CEAVP+ACVPatronal+riesgostrabajo) CuotasPatronales, "
                    "(ExcedenteObrero+PrestObrero+GMPO+InvalidezVO+CEAVObrero) CuotasObrero "
                    "from ("
                    "select id, uma, DOF, FactIntg, uma3, SDI, cuotafija, "
                    "case "
	                "when (((SDI*" + dias + ")-uma3)*(select ExcedentePatronal from conciliacion_datospatronimss)/100) < 0 then 0 else (((SDI*" + dias + ")-uma3)*(select ExcedentePatronal from conciliacion_datospatronimss)/100) "
                    "end ExcedentePatronal, "
                    "(SDI*" + dias + ")*(select Prestaciones from conciliacion_datospatronimss)/100 PrestDineat, "
                    "(SDI*" + dias + ")*(select GMPP from conciliacion_datospatronimss)/100 GMPP, "
                    "(SDI*" + dias + ")*(select Invalidez from conciliacion_datospatronimss)/100 InvalidezVP, "
                    "(SDI*" + dias + ")*(select Guarderias from conciliacion_datospatronimss)/100 Guarderias, "
                    "(SDI*" + dias + ")*(select Retiro from conciliacion_datospatronimss)/100 Retiro, "
                    "(SDI*" + dias + ")*(select CEAV from conciliacion_datospatronimss)/100 CEAVP, "
                    "(SDI*" + dias + ")*(select ACVPatronal from conciliacion_datospatronimss)/100 ACVPatronal, "
                    "case "
                        "when (((SDI*" + dias + ")-uma3)*(select ExcedenteObrero from conciliacion_datosobrero)/100) < 0 then 0 else " "(((SDI*" + dias + ")-uma3)*(select ExcedenteObrero from conciliacion_datosobrero)/100) "
                    "end ExcedenteObrero, "
                    "(SDI*" + dias + ")*(select PrestacionesObrero from conciliacion_datosobrero)/100 PrestObrero, "
                    "(SDI*" + dias + ")*(select GMPO from conciliacion_datosobrero)/100 GMPO, "
                    "(SDI*" + dias + ")*(select RiesgosTrabajo from conciliacion_datosobrero) RiesgosTrabajo, "
                    "(SDI*" + dias + ")*(select InvalidezVO from conciliacion_datosobrero)/100 InvalidezVO, "
                    "(SDI*" + dias + ")*(select CEAVObrero from conciliacion_datosobrero)/100 CEAVObrero "
                    "from ( "
                    "select *, "
                    "case  "
                        "when DOF*FactIntg > (select uma*25 from conciliacion_uma) then (select uma*25 from conciliacion_uma) else DOF*FactIntg   "
                    "end SDI, "
                    "((uma*" + dias + ")*(select CuotaFija from conciliacion_datospatronimss))/100 CuotaFija "
                    "from  "
                    "(select 1 as id, (select UMA from conciliacion_uma) uma, " + monto + "/30 DOF, " "((Aguinaldo/365)+((DVacaciones/365)*PVacacional))+Antiguedad FactIntg, (select UMA*3* " + dias + " from conciliacion_uma) uma3  "
                    "from conciliacion_factorintegracion)tbl)tbl)tbl")

        print(factInt)        
    
    context = {
        "titulo" : title,
        "monto" : monto,
        "factInt" : factInt,        
        "dias" : dias,
    }

    return render(request, "calcIMSS.html", context)


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

@login_required(login_url='/')
def receipts(request):

    frmNombre = request.POST.get("Cliente", "")
    frmRFC = request.POST.get("RFC", "")
    frmAño = request.POST.get("Anio", "")
    frmMes = request.POST.get("Mes", "")
    frmTrue = request.POST.get("frmEnvia", "")
    queryset = ""
    items = ""
    txtInicial = ""

    titulo = "Reporte de facturas recibidas"

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

    if request.POST.get("frmEnvia", "") == "":
        txtInicial = "Selecciona un filtro para mostrar las facturas"
    else:
        queryset = Comprobante.objects.raw("select 1 as id, upper(b.Nombre) Nombre, a.SubTotal, ROUND(a.Total-a.SubTotal, 2) IVA, Total, c.Descripcion, "
                                           "d.TasaOCuota*100 TasaOCuota, d.Importe, b.Rfc, a.TipoCambio, "
                                           "Moneda, a.UUIDInt, YEAR(Fecha) Periodo, DATE_FORMAT(Fecha, CONCAT(char(37), 'm')) Mes "
                                           "from conciliacion_comprobante a "
                                           "inner join conciliacion_receptor b "
                                           "on a.IDKey = b.IDKey "
                                           "inner join conciliacion_concepto c "
                                           "on a.IDKey = c.IDKey "
                                           "left join conciliacion_traslado d "
                                           "on a.IDKey = d.IDKey "
                                           "where a.TipoEmRe = 'Recibidas' "
                                           + RFCFiltro
                                           + NombreFiltro
                                           + AñoFiltro
                                           + MesFiltro
                                           + " group by a.UUIDInt "
                                           + "order by Fecha desc, Nombre Limit 10"
                                           )
        #print(queryset)
        
        paginator = Paginator(queryset, 15)
        page = request.GET.get("page")
        
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)

    rfc = Emisor.objects.raw(
        "select distinct 1 as id, Rfc from conciliacion_receptor order by 2"
    )
    print(rfc)
    anio = Comprobante.objects.raw(
        "select distinct 1 as id, year(Fecha) Año from conciliacion_comprobante order by 2"
    )
    mes = Comprobante.objects.raw(
        'select distinct 1 as id, DATE_FORMAT(Fecha, CONCAT(char(37), "m")) Mes from conciliacion_comprobante order by cast(month(Fecha) as int)'
    ) 

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
        "txt" : txtInicial,
    }

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

@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
def conciliacion(request):

    titulo = "Conciliación"

    rfc = Balance.objects.raw("select DISTINCT 1 as id, a.RFC, b.Nombre "
                              "from conciliacion_balance a "
                              "inner join conciliacion_emisor b "
                              "on a.RFC = b.Rfc "
                              "group by RFC ")

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
    print(rfc)

    return render(request, "conciliacion.html", context)

@login_required(login_url='/')
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


def export_data(request):
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="Conciliacion.xlsx"'

    # create workbook
    wb = Workbook()
    sheet = wb.active

    # export data to Excel
    # rows = .objects.all().values_list('')
    rows = Comprobante.objects.filter(TipoEmRe='Recibidas')
    print(rows.query)

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
