from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.db.models.functions import Substr
from django.db.models import Sum
from django.db import connection

from .models import InvoiceEmitidas, InvoiceRecibidas, Balance

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import String
import sys

# Create your views here.

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                do_login(request, user)
                return redirect('/menu')
    return render(request, 'login.html')

def logout(request):
    do_logout(request)
    return redirect('/')

def menu(request):

    titulo = "Olvera Contadores y Asociados"

    context = {
        "titulo" : titulo,
    }

    return render(request, 'menu.html', context)

def invoice(request):

    titulo = "Importar facturas emitidas"    
    file = ""
    hideForm = 0

    if request.method == 'POST': 
                
        new_invoice = request.FILES['xlsfile']
        
        try:
            df = pd.read_excel(new_invoice, sheet_name='Emitidos (2)')
            print(df)
            engine = create_engine('mysql://birkoff:awgUGF7812$.@10.87.35.3/olvera')
            df.to_sql('conciliacion_invoiceemitidas', con=engine, if_exists='append', index=False)
            
        except Exception:
            file = "Hubo un error al subir el archivo, favor de comunicarse con el administrador"
            print(file)
            e = sys.exc_info()
            print(e)

        finally:
            hideForm = 1   
            file = "El archivo subió correctamente"
    
    context = {
        "titulo" : titulo,
        "file" : file,
        "hideForm" : hideForm,
    }           

    return render(request, 'importar.html', context)

def receipts(request):
    
    titulo = "Importar facturas recibidas"
    file = ""
    hideForm = 0
    
    if request.method == 'POST':
        
        new_receipt = request.FILES['xlsfile']
        
        try:
            df = pd.read_excel(new_receipt, sheet_name='Recibidas (2)')
            print(df)
            engine = create_engine('mysql://birkoff:awgUGF7812$.@10.87.35.3/olvera')
            df.to_sql('conciliacion_invoicerecibidas', con=engine, if_exists='append', index=False)
            
        except Exception:
            file = "Hubo un error al subir el archivo, favor de comunicarse con el administrador"
            print(file)
            e = sys.exc_info()
            print(e)

        finally:
            hideForm = 1   
            file = "El archivo subió correctamente"        
    
    context = {
        "titulo" : titulo,
        "file" : file,
        "hideForm" : hideForm,
    }
        
    return render(request, 'recibidas.html', context)

def customers(request):
    titulo = "Clientes"
    user = request.user

    #queryset = Invoice.objects.all().order_by('Nombre_Receptor').filter(Nombre_Receptor='Carlos Enrique Ortega Mora')

    queryset = InvoiceEmitidas.objects.values('RFC_Receptor', 'Moneda'
            ).order_by('RFC_Receptor'
                       ).annotate(total_price=Sum('Total')
                                 )#.filter(Nombre_Receptor='Carlos Enrique Ortega Mora')

    #print(queryset.query)

    context = {
        "titulo" : titulo,
        "usr"    : user,
        "qry"    : queryset,
    }

    return render(request, 'clientes.html', context)

def repEmitidas(request):
    titulo = "Reporte Facturas Emitidas"
    
    queryset = InvoiceEmitidas.objects.raw('''select id, Mes, Año, sum(SubTotal) SubTotal, sum(IVA_16) IVA_16, sum(Total) Total  from (
                                    select id, Fecha_Emision, SubTotal, IVA_16, Total, SUBSTR(Fecha_Emision, 4, 2) Mes, SUBSTR(Fecha_Emision, 7, 4) Año, timestamp 
                                    from conciliacion_invoiceemitidas                                    
                                    ) tbl
                                    group by Mes, Año
                                    order by 3, 2''')
    """
    queryset = Invoice.objects.values('Fecha_Emision', 'IVA_16', 'Total'
            ).annotate(Sub_Total=Sum('SubTotal')
                       )
                       """
    #print(queryset.query)
    
    context = {
        "titulo" : titulo,
        "qry" : queryset
    }
    return render(request, 'emitidas.html', context)

def repRecibidas(request):
    titulo = "Reporte Facturas Recibidas"

    queryset = InvoiceRecibidas.objects.raw('''select id, Mes, Año, sum(SubTotal) SubTotal, Sum(IVA_16) IVA_16, 
                                    Sum(Retenido_IVA) Retenido_IVA, Sum(Retenido_ISR) Retenido_ISR, Sum(Total) Total from 
                                    (select id, Fecha_Emision, SUBSTR(Fecha_Emision, 4,2) Mes, SUBSTR(Fecha_Emision, 7, 4) Año, 
                                    SubTotal, IVA_16, Retenido_IVA, Retenido_ISR, Total from conciliacion_invoicerecibidas
                                    ) tbl
                                    group by Mes, Año
                                    Order by 3, 2''')

    context = {
        "titulo" : titulo,
        "qry" : queryset
    }

    return render(request, 'factRecibidas.html', context)

def impConciliacion(request):

    titulo = "Importar balanza de comprobación"  
    file = ""
    hideForm = 0
    
    queryset = Balance.objects.values('Mes').distinct().order_by('Mes')
    
    print(queryset.query)

    if request.method == 'POST':
        ##balance_resource = BalanceResource()
        ##ds = Dataset()
        new_conciliacion = request.FILES['xlsfile']
        #mes = form.cleaned_data['mes']
        mes = request.POST.get('mes', '')
        
        print('Este es el mes que yo quiero importar: ' + mes)
        #imported_data = ds.load(new_conciliacion.read())
        try:
            df = pd.read_excel(new_conciliacion, sheet_name=mes)
            print(df)        
           
            engine = create_engine('mysql://birkoff:awgUGF7812$.@192.168.0.14/olvera')            
            df.to_sql('conciliacion_balance', con=engine, if_exists='append', index=False)
            
        except Exception:
            file = "Hubo un error al subir el archivo, favor de comunicarse con el administrador"
            print(file)
            e = sys.exc_info()
            print(e)
        #new_receipts = request.FILES['xlsfile']
        #imported_data = ds.load(new_receipts.read())
        
        

        ##result = balance_resource.import_data(ds, dry_run=True)        
        ##if not result.has_errors():
            # Import now
            ##balance_resource.import_data(ds, dry_run=False)
            ##hideForm = 1   
            ##file = "El archivo subió correctamente"
        finally:            
            hideForm = 1   
            file = "El archivo subió correctamente"
            
    context = {
        "titulo" : titulo,
        "file" : file,
        "hideForm" : hideForm,
        "queryset" : queryset,
    }   

    return render(request, 'importBalanza.html', context)

def conciliacion(request, cuenta, campo_1, campo_2, tabla, title_1, title_2):
    titulo = "Conciliación"
    count = cuenta
    
    if request.method == 'GET':
        r105 = InvoiceEmitidas.objects.raw("""select id, Cuenta, Mes, Año, Sum(""" + campo_1 + """) campo_1, """ + campo_2 + """ campo_2, (Sum(""" + campo_1 + """) - """ + campo_2 + """) Diff from (
                                    select a.id, Cuenta, SUBSTR(a.Fecha_Emision, 4, 2) Mes, SUBSTR(a.Fecha_Emision, 7, 4) Año, a.""" + campo_1 + """, b.""" + campo_2 + """ 
                                    from """ + tabla + """ a 
                                    inner join conciliacion_balance b
                                    on SUBSTR(a.Fecha_Emision, 4, 2) = case when LENGTH(b.Mes) = 1 then Concat('0', b.Mes) when LENGTH(b.Mes) = 2 then b.Mes end
                                    and SUBSTR(a.Fecha_Emision, 7, 4) = b.Año
                                    where Cuenta = '""" + cuenta + """'
                                    ) tbl
                                    group by Mes, Año, """ + campo_2 + """, Cuenta
                                    """)
    context = {
        "titulo" : titulo,
        "r105" : r105,
        "title_1" : title_1,
        "title_2" : title_2,
        "cuenta" : count,
    }

    return render(request, 'conciliacion.html', context)

def impbalanza(request):
    
    titulo = "Archivos cargados"
    
    balanzas = Balance.objects.values('Mes', 'Año', 'timestamp').distinct()
    emitidas = InvoiceEmitidas.objects.raw("select DISTINCT 1 id, timestamp,  replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') fecha from conciliacion_invoiceemitidas")
    recibidas = InvoiceRecibidas.objects.raw("select DISTINCT 1 id, timestamp, replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') fecha from conciliacion_invoicerecibidas")
    
    context = {
        "titulo" : titulo,
        'balanzas' : balanzas,
        'emitidas' : emitidas,
        'recibidas' : recibidas,
    }    
    
    return render(request, 'balanzasCargadas.html', context)

def delete_balanza(request, balanza_id):
    
    delete = str(balanza_id)
            
    try:
        #selBalanza = Balance.objects.get(Concat(Mes, Año) = delete)
        #selBalanza = Balance.objects.raw("delete from conciliacion_balance where CONCAT(Mes, Año) = '" + delete + "'")
        #print(selBalanza)        
        
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM conciliacion_balance WHERE CONCAT(Mes, Año) = '" + delete + "'")
            #"DELETE FROM mydb_mymodel WHERE s_type = '%s' AND barcode = '%s' AND shopcode = '%s' AND date = '%s'" ,
            #[d.s_type,d.barcode,d.shopcode,d.date]
        #)            
    except Balance.DoesNotExist:        
        #print('No jalo :(')
        return redirect('menu')
    
    #selBalanza.delete()
    
    return redirect('impbalanza')

def delete_factemitidas(request, factemitidas_id):
    
    factura = str(factemitidas_id)
    
    try:
        with connection.cursor() as cursor:            
            #cursor = "select DISTINCT timestamp from conciliacion_invoiceemitidas where replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') = '" + factura + "'"        
            cursor.execute("delete from conciliacion_invoiceemitidas where replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') = '" + factura + "'")
            print(cursor)
        
    except InvoiceEmitidas.DoesNotExist:        
        #print('No jalo :(')
        return redirect('menu')
    
    finally:
        print('Eliminicación de facturas emitidas con fecha: ' + factura)
    
    return redirect('impbalanza')

def delete_factrecibidas(request, factrecibidas_id):
    
    factura = str(factrecibidas_id)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("delete from conciliacion_invoicerecibidas where replace(replace(replace(cast(timestamp as char), ' ', ''),'-',''),':', '') = '" + factura + "'")
            print(cursor)
            
    except InvoiceRecibidas.DoesNotExist:        
        #print('No jalo :(')
        return redirect('menu')
    
    finally:
        print('Eliminicación de facturas emitidas con fecha: ' + factura)
        
    return redirect('impbalanza')

"""
def export_data(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Data.xlsx"'
    
    # create workbook
    wb = Workbook()
    sheet = wb.active
    
    # export data to Excel
    rows = models.Data.objects.all().values_list(
    
    wb.save(response)

    return response"""


def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        employee_resource = EmployeeResource()
        dataset = Dataset()
        new_employees = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='csv')
            result = employee_resource.import_data(dataset, dry_run=True)                                                                 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_employees.read().decode('utf-8'),format='json')
            # Testing data import
            result = employee_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            # Import now
            employee_resource.import_data(dataset, dry_run=False)

    return render(request, 'import.html')