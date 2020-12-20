from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout

from tablib import Dataset

from .resources import InvoiceResource
from .models import Invoice

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

    return render(request, 'menu.html')

def invoice(request):

    titulo = "Importar facturas"

    context = {
        "titulo" : titulo,
    }

    if request.method == 'POST':
        invoice_resource = InvoiceResource()        
        ds = Dataset()
        new_invoice = request.FILES['xlsfile']
        #print(new_invoice)
        imported_data = ds.load(new_invoice.read())
        print(imported_data)
        result = invoice_resource.import_data(ds, dry_run=True)

        if not result.has_errors():
            # Import now
            invoice_resource.import_data(ds, dry_run=False)

    return render(request, 'importar.html', context)

def customers(request):
    titulo = "Clientes"
    user = request.user

    queryset = Invoice.objects.all()

    print(queryset.query)


    context = {
        "titulo" : titulo,
        "usr"    : user,
        "qry"    : queryset,
    }

    return render(request, 'clientes.html', context)




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