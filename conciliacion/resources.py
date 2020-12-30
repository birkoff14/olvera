from import_export import resources  
from .models import InvoiceEmitidas, InvoiceRecibidas, Balance

class InvoiceEmitidasResource(resources.ModelResource):
    class Meta:
        model = InvoiceEmitidas
        
class InvoiceRecibidasResource(resources.ModelResource):
    class Meta:
        model = InvoiceRecibidas

class BalanceResource(resources.ModelResource):
    class Meta:
        model = Balance
