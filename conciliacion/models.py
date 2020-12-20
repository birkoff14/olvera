from django.db import models

# Create your models here.

class Invoice(models.Model):
    Estado_SAT = models.CharField(max_length=150, blank=True)
    Version = models.CharField(max_length=150, blank=True)
    Tipo = models.CharField(max_length=150, blank=True)
    Fecha_Emision = models.CharField(max_length=150, blank=True)
    Fecha_Timbrado = models.CharField(max_length=150, blank=True)
    Serie = models.CharField(max_length=150, blank=True)
    Folio = models.CharField(max_length=150, blank=True)
    UUID = models.CharField(max_length=150, blank=True)
    RFC_Receptor = models.CharField(max_length=150, blank=True)
    Nombre_Receptor = models.CharField(max_length=150, blank=True)
    UsoCFDI = models.CharField(max_length=150, blank=True)
    SubTotal  = models.CharField(max_length=150, blank=True)
    IVA_16 = models.CharField(max_length=150, blank=True)
    Total = models.CharField(max_length=150, blank=True)
    Total_Trasladados = models.CharField(max_length=150, blank=True)
    Moneda = models.CharField(max_length=150, blank=True)
    Forma_De_Pago = models.CharField(max_length=150, blank=True)
    Metodo_de_Pago = models.CharField(max_length=150, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Fecha")