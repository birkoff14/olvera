from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout

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

    return render(request, 'menu.html')

def invoice(request):

    titulo = "Importar facturas"

    context = {
        "titulo" : titulo,
    }

    if request.method == 'POST':
        invoice_resource = InvoiceResource()
        databook = Databook()
        ds = Dataset()
        new_invoice = request.FILES('xlsfile')
        imported_data = ds.load(new_invoice.read())
        #result = invoice_resource.imported_data(ds, dry_run=False)

        for dataset in imported_data.sheets():
            print(dataset.title)  # returns the names of the sheets
            print(dataset)  # returns the data in each sheet


    return render(request, 'importar.html', context)

def customers(request):
    titulo = "Clientes"
    user = request.user

    context = {
        "titulo" : titulo,
        "usr"    : user
    }

    return render(request, 'clientes.html', context)