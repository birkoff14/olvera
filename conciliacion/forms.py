from django import forms
from django.contrib.auth.models import User
from .models import InvoiceEmitidas, DatosFactura, InProyecto, FormaPago, Balance, InContabilidad
from django.forms import ModelChoiceField
import datetime
from .services import cuentasContables

class RFC(forms.ModelForm):
    class Meta:
        model = InvoiceEmitidas
        fields = ["Nombre_Emisor", "RFC_Emisor"]
        
        
    RFC_Emisor = forms.ModelChoiceField(label="RFC", queryset=InvoiceEmitidas.objects.all().values_list('RFC_Emisor').distinct())
    #forms.ModelChoiceField(label="RFC", queryset=InvoiceEmitidas.objects.values('RFC_Emisor').distinct())
    
    def clean_rfc(self):
        RFC_Emisor = self.cleaned_data.get("RFC_Emisor")
        RFC_Emisor.replace("'", "")
        return RFC_Emisor
    
class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class addDatos(forms.ModelForm):
    class Meta:
        model = DatosFactura
        fields = ["ProyectoCont", "Contabilidad", "FechaPago", "FormaPago", "Notas", "CuentaContable", "idUsuario", "UUIDInt"]
        
    #InProyecto = forms.ModelChoiceField(label="Ingresos proyectos", queryset=InProyecto.objects.all().values_list('InProyecto').distinct())
    ProyectoCont = forms.ModelChoiceField(label="Proyectos contabilidad", queryset=InProyecto.objects.all().order_by('InProyecto'))
    Contabilidad = forms.ModelChoiceField(label="Ingresos Contabilidad", queryset=InContabilidad.objects.all())
    #GaProyecto = forms.ModelChoiceField(label="Gastos Proyecto", queryset=GaProyecto.objects.all())
    #GaContabilidad = forms.ModelChoiceField(label="Gastos Contabilidad", queryset=GaContabilidad.objects.all())
    #idUsuario = forms.ModelChoiceField(label="Usuario", queryset=User.objects.all())
    UUIDInt = forms.CharField(widget = forms.HiddenInput())
    #FechaPago = forms.CharField(label='Fecha de pago')
    FechaPago = forms.DateTimeField(initial=datetime.date.today().strftime("%Y-%m-%d"), required=False, label="Fecha de pago")
    FormaPago = forms.ModelChoiceField(label="Forma de pago", queryset=FormaPago.objects.all().order_by('FormaPago'))
    Notas = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), required=False)
    #CuentaContable = forms.ModelChoiceField(label="Cuenta contable", queryset=Balance.objects.values_list('Cuenta', flat=True).order_by('Cuenta').distinct())
    #CC = forms.ModelChoiceField(label="Cuenta contable", queryset=Balance.objects.all().distinct())
    #CHOICES = (('Option 1', 'Option 1'),('Option 2', 'Option 2'),)
    CuentaContable = forms.CharField(label="Cuenta contable")
    #idUsuario = forms.ModelChoiceField(label="Usuario", queryset=User.objects.all())
    idUsuario = UserModelChoiceField(label="Usuario", queryset=User.objects.filter(is_active=True))

    #def __init__(self, *args, **kwargs):
    #    super(addDatos, self).__init__(*args, **kwargs)
    #    self.fields['id'].queryset = Balance.objects.all()