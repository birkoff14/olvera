from django import forms
from .models import InvoiceEmitidas

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