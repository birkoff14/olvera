from django import forms
from django.contrib.auth.models import User
from .models import InvoiceEmitidas, DatosFactura, InProyecto, InContabilidad, GaProyecto, GaContabilidad

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

class addDatos(forms.ModelForm):
    class Meta:
        model = DatosFactura
        fields = ["InProyecto", "InContabilidad", "GaProyecto", "GaContabilidad", "idUsuario", "UUIDInt"]
        
    #InProyecto = forms.ModelChoiceField(label="Ingresos proyectos", queryset=InProyecto.objects.all().values_list('InProyecto').distinct())
    InProyecto = forms.ModelChoiceField(label="Ingresos Proyecto", queryset=InProyecto.objects.all())
    InContabilidad = forms.ModelChoiceField(label="Ingresos Contabilidad", queryset=InContabilidad.objects.all())
    GaProyecto = forms.ModelChoiceField(label="Gastos Proyecto", queryset=GaProyecto.objects.all())
    GaContabilidad = forms.ModelChoiceField(label="Gastos Contabilidad", queryset=GaContabilidad.objects.all())
    idUsuario = forms.ModelChoiceField(label="Usuario", queryset=User.objects.all())
    UUIDInt = forms.CharField(label='Descripción')
