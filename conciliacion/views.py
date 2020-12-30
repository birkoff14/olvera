from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.db.models.functions import Substr
from django.db.models import Sum

from .resources import InvoiceEmitidasResource, InvoiceRecibidasResource, BalanceResource
from .models import InvoiceEmitidas, InvoiceRecibidas, Balance

from tablib import Dataset

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

    context = {
        "titulo" : titulo,
    }

    if request.method == 'POST':        

        invoice_resource = InvoiceEmitidasResource()        
        ds = Dataset()
        #db = Databook()
        new_invoice = request.FILES['xlsfile']
        #pt = request.FILES['xlsfile'].file.name
        #print(pt)
        #databook = tablib.Databook().load('xlsx', open('file.xlsx', 'rb').read())
        #databook = db.load(new_invoice.read())
        imported_data = ds.load(new_invoice.read())        
        print(imported_data)
        
        result = invoice_resource.import_data(ds, dry_run=True)
        
        if not result.has_errors():
            # Import now
            invoice_resource.import_data(ds, dry_run=False)        

    return render(request, 'importar.html', context)

def receipts(request):
    titulo = "Importar facturas recibidas"
    
    context = {
        "titulo" : titulo
    }
    
    if request.method == 'POST':
        receipts_resource = InvoiceRecibidasResource()
        ds = Dataset()
        new_receipts = request.FILES['xlsfile']
        imported_data = ds.load(new_receipts.read())
        #print(imported_data)
        
        result = receipts_resource.import_data(ds, dry_run=True)        
        if not result.has_errors():
            # Import now
            receipts_resource.import_data(ds, dry_run=False)
            
    #if request.method == "POST":
    #    file = request.FILES['xlsfile']
    #    print(file)
    #    wb = load_workbook(filename=file)
    #    print(wb.sheetnames)
        
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

    context = {
        "titulo" : titulo
    }

    if request.method == 'POST':
        balance_resource = BalanceResource()
        ds = Dataset(['11'])
        new_conciliacion = request.FILES['xlsfile']
        imported_data = ds.load(new_conciliacion.read())
        
        #new_receipts = request.FILES['xlsfile']
        #imported_data = ds.load(new_receipts.read())
        
        print(ds)

        result = balance_resource.import_data(ds, dry_run=True)        
        if not result.has_errors():
            # Import now
            balance_resource.import_data(ds, dry_run=False)

    return render(request, 'importBalanza.html', context)

def conciliacion(request, cuenta, campo_1, campo_2, tabla, title_1, title_2):
    titulo = "Conciliación"
    #title_1 = request.GET['title_1']
    #title_2 = request.GET['title_2']
    
    if request.method == 'GET':
        r105 = InvoiceEmitidas.objects.raw("""select id, Cuenta, Mes, Año, Sum(""" + campo_1 + """) campo_1, """ + campo_2 + """ campo_2, (Sum(""" + campo_1 + """) - """ + campo_2 + """) Diff from (
                                    select a.id, Cuenta, SUBSTR(a.Fecha_Emision, 4, 2) Mes, SUBSTR(a.Fecha_Emision, 7, 4) Año, a.""" + campo_1 + """, b.""" + campo_2 + """ 
                                    from """ + tabla + """ a 
                                    inner join conciliacion_balance b
                                    on SUBSTR(a.Fecha_Emision, 4, 2) = b.Mes
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
    }
    
    #print(r105)

    return render(request, 'conciliacion.html', context)
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
