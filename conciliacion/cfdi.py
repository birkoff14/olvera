from xml.dom.minidom import parse, parseString
import mysql.connector
import os
import pathlib
import sys
import uuid
####
import fnmatch
import os.path
import re

#import pdb; pdb.set_trace()

config = {
  'user': 'birkoff',
  'password': 'awgUGF7812$.',
  #'host': '192.168.0.21',
  'host': '10.87.35.60',
  'database': 'olvera',
  'raise_on_warnings': True
}

#Función que busca el UUID del archivo XML
def buscaUUID(search):
    
    for skill in search:
        
        ID_UUID = skill.getAttribute("UUID")
        #print(ID_UUID)
        
        return ID_UUID
        #                                            skill.getAttribute("FechaTimbrado"),
        #                                            skill.getAttribute("RfcProvCertif"),
        #                                            skill.getAttribute("NoCertificadoSAT"),
        #                                            str(UUID))
                        
        #                cursor.execute(add_TimbreFiscalDigital, data_TimbreFiscalDigital)


directorio = 'xml/test'

def main():
    idFile = 0
    
    for root, dirs, files in os.walk(directorio):
        for ark in files:
            if fnmatch.fnmatch(ark,'*.xml'):  

                path = root + "/" + ark    

                cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor(buffered=True)                
                doc = parse(path)


                VerificaUUID = doc.getElementsByTagName("tfd:TimbreFiscalDigital")   
                x = buscaUUID(VerificaUUID)             
                #print(x)

                #try:
                existeArchivo = "select count(*) from conciliacion_comprobante where UUIDInt = '" + x + "';"
                #print(existeArchivo)
                cursor.execute(existeArchivo)
                resp = cursor.fetchone()
                number = number_of_rows=resp[0]

                #print(number)

                if number == 0:

                    try:  

                        idFile = idFile + 1

                        #doc = parse(path)

                        UUID = x
                        print(str(idFile) + ".- Cargando archivo: " + str(UUID))

                        Comprobante = doc.getElementsByTagName("cfdi:Comprobante")
                        Emisor = doc.getElementsByTagName("cfdi:Emisor")
                        Receptor = doc.getElementsByTagName("cfdi:Receptor")
                        Concepto = doc.getElementsByTagName("cfdi:Concepto")
                        Pago = doc.getElementsByTagName("pago10:Pago")
                        DoctoRelacionado = doc.getElementsByTagName("pago10:DoctoRelacionado")
                        Impuestos = doc.getElementsByTagName("cfdi:Impuestos")
                        Traslado = doc.getElementsByTagName("cfdi:Traslado")
                        TimbreFiscalDigital = doc.getElementsByTagName("tfd:TimbreFiscalDigital")

                        #Nomina

                        Nomina = doc.getElementsByTagName("nomina12:Nomina")
                        NEmisor = doc.getElementsByTagName("nomina12:Emisor")
                        NReceptor = doc.getElementsByTagName("nomina12:Receptor")
                        NPercepciones = doc.getElementsByTagName("nomina12:Percepciones")
                        NPercepcion = doc.getElementsByTagName("nomina12:Percepcion")
                        OtroPago = doc.getElementsByTagName("nomina12:OtrosPagos")
                        SubsidioAlEmpleo = doc.getElementsByTagName("nomina12:SubsidioAlEmpleo")

                        for skill in Comprobante:

                            add_comprobante = ("insert into conciliacion_comprobante" 
                                            "(Version, Serie, Folio, Fecha, FormaPago, NoCertificado, Subtotal, Moneda, Total, TipoDeComprobante, MetodoPago, LugarExpedicion, UUIDInt) "
                                            "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                            data_comprobante = (skill.getAttribute("Version"), 
                                                skill.getAttribute("Serie"), 
                                                skill.getAttribute("Folio"), 
                                                skill.getAttribute("Fecha"), 
                                                skill.getAttribute("FormaPago"), 
                                                skill.getAttribute("NoCertificado"),
                                                skill.getAttribute("SubTotal"), 
                                                skill.getAttribute("Moneda"), 
                                                skill.getAttribute("Total"), 
                                                skill.getAttribute("TipoDeComprobante"), 
                                                skill.getAttribute("MetodoPago"), 
                                                skill.getAttribute("LugarExpedicion"), 
                                                str(UUID))

                            cursor.execute(add_comprobante, data_comprobante)

                        for skill in Emisor:
                            add_emisor = ("insert into conciliacion_emisor "
                                        "(Rfc, Nombre, RegimenFiscal, UUIDInt) "
                                        "values (%s, %s, %s, %s)")

                            data_emisor = (skill.getAttribute("Rfc"), 
                                        skill.getAttribute("Nombre"), 
                                        skill.getAttribute("RegimenFiscal"), 
                                        str(UUID))

                            cursor.execute(add_emisor, data_emisor)

                        for skill in Receptor:

                            add_receptor = ("insert into conciliacion_receptor "
                                        "(Rfc, Nombre, UsoCFDI, UUIDInt) " 
                                        "values (%s, %s, %s, %s)")

                            data_receptor = (skill.getAttribute("Rfc"), 
                                            skill.getAttribute("Nombre"), 
                                            skill.getAttribute("UsoCFDI"), 
                                            str(UUID))

                            cursor.execute(add_receptor, data_receptor)

                        for skill in Concepto:

                            add_concepto = ("insert into conciliacion_concepto "
                                        "(ClaveProdServ, NoIdentificacion, Cantidad, ClaveUnidad, Unidad, Descripcion, ValorUnitario, Importe, UUIDInt) "
                                        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

                            data_concepto = (skill.getAttribute("ClaveProdServ"), 
                                            skill.getAttribute("NoIdentificacion"), 
                                            skill.getAttribute("Cantidad"), 
                                            skill.getAttribute("ClaveUnidad"), 
                                            skill.getAttribute("Unidad"), 
                                            skill.getAttribute("Descripcion"), 
                                            skill.getAttribute("ValorUnitario"), 
                                            skill.getAttribute("Importe"), 
                                            str(UUID))

                            cursor.execute(add_concepto, data_concepto)

                        for skill in Pago:

                            print("Paguito: " + skill.getAttribute("FechaPago"))

                            add_Pago = ("insert into conciliacion_pago "
                                    "(FechaPago, FormaDePagoP, MonedaP, Monto, NumOperacion, UUIDInt) "
                                    "values (%s, %s, %s, %s, %s, %s)")

                            data_Pago = (skill.getAttribute("FechaPago"), 
                                        skill.getAttribute("FormaDePagoP"), 
                                        skill.getAttribute("MonedaP"), 
                                        skill.getAttribute("Monto"), 
                                        skill.getAttribute("NumOperacion"), 
                                        str(UUID))

                            cursor.execute(add_Pago, data_Pago)

                        for skill in DoctoRelacionado:

                            add_DoctoRelacionado = ("insert into conciliacion_doctorelacionado "
                                                    "(IdDocumento, Folio, Serie, MonedaDR, MetodoDePagoDR, NumParcialidad, ImpSaldoAnt, ImpPagado, ImpSaldoInsoluto, UUIDInt) "
                                                    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                            data_DoctoRelacionado = (skill.getAttribute("IdDocumento"),
                                                    skill.getAttribute("Folio"),
                                                    skill.getAttribute("Serie"),
                                                    skill.getAttribute("MonedaDR"),
                                                    skill.getAttribute("MetodoDePagoDR"),
                                                    skill.getAttribute("NumParcialidad"),
                                                    skill.getAttribute("ImpSaldoAnt"),
                                                    skill.getAttribute("ImpPagado"),
                                                    skill.getAttribute("ImpSaldoInsoluto"),
                                                    str(UUID))

                            cursor.execute(add_DoctoRelacionado, data_DoctoRelacionado)

                        for skill in Impuestos:

                            add_Impuestos = ("insert into conciliacion_impuestos "
                                            "(TotalImpuestosTrasladados, UUIDInt)" 
                                            "values (%s, %s)")

                            data_Impuestos = (skill.getAttribute("TotalImpuestosTrasladados"),
                                            str(UUID))

                            cursor.execute(add_Impuestos, data_Impuestos)

                        for skill in Traslado:

                            add_Traslado = ("insert into conciliacion_traslado "
                                            "(Base, Impuesto, TipoFactor, TasaOCuota, Importe, UUIDInt) "
                                            "values (%s, %s, %s, %s, %s, %s)")

                            data_Traslado = (skill.getAttribute("Base"),
                                            skill.getAttribute("Impuesto"),
                                            skill.getAttribute("TipoFactor"),
                                            skill.getAttribute("TasaOCuota"),
                                            skill.getAttribute("Importe"),
                                            str(UUID))

                            cursor.execute(add_Traslado, data_Traslado)

                        for skill in TimbreFiscalDigital:

                            add_TimbreFiscalDigital = ("insert into conciliacion_timbrefiscaldigital "
                                                    "(Version, UUID, FechaTimbrado, RfcProvCertif, NoCertificadoSAT, UUIDInt) "
                                                    "values (%s, %s, %s, %s, %s, %s)")

                            data_TimbreFiscalDigital = (skill.getAttribute("Version"),
                                                        skill.getAttribute("UUID"),
                                                        skill.getAttribute("FechaTimbrado"),
                                                        skill.getAttribute("RfcProvCertif"),
                                                        skill.getAttribute("NoCertificadoSAT"),
                                                        str(UUID))

                            cursor.execute(add_TimbreFiscalDigital, data_TimbreFiscalDigital)

                        for skill in Nomina:

                            add_Nomina = ("insert into conciliacion_nomina "
                                        "(FechaFinalPago, FechaInicialPago, FechaPago, NumDiasPagados, TipoNomina, TotalOtrosPagos, TotalPercepciones, Version, UUIDInt) "
                                        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)")


                            data_Nomina = (skill.getAttribute("FechaFinalPago"),
                                        skill.getAttribute("FechaInicialPago"),
                                        skill.getAttribute("FechaPago"),
                                        skill.getAttribute("NumDiasPagados"),
                                        skill.getAttribute("TipoNomina"),
                                        skill.getAttribute("TotalOtrosPagos"),
                                        skill.getAttribute("TotalPercepciones"),
                                        skill.getAttribute("Version"),
                                        str(UUID))

                            cursor.execute(add_Nomina, data_Nomina)

                        for skill in NEmisor:

                            add_NEmisor = ("insert into conciliacion_nemisor "
                                        "(RegistroPatronal, UUIDInt)" 
                                        "values (%s, %s)")

                            data_NEmisor = (skill.getAttribute("RegistroPatronal"),
                                            str(UUID))

                            cursor.execute(add_NEmisor, data_NEmisor)

                        for skill in NReceptor:

                            add_NReceptor = ("insert into conciliacion_nreceptor "
                                        "(Antigüedad, ClaveEntFed, Curp, Departamento, FechaInicioRelLaboral, NumEmpleado, NumSeguridadSocial, PeriodicidadPago, Puesto, RiesgoPuesto, SalarioBaseCotApor, SalarioDiarioIntegrado, Sindicalizado, TipoContrato, TipoJornada, TipoRegimen, UUIDInt) "
                                        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                            data_NReceptor = (skill.getAttribute("Antigüedad"),
                                            skill.getAttribute("ClaveEntFed"),
                                            skill.getAttribute("Curp"),
                                            skill.getAttribute("Departamento"),
                                            skill.getAttribute("FechaInicioRelLaboral"),
                                            skill.getAttribute("NumEmpleado"),
                                            skill.getAttribute("NumSeguridadSocial"),
                                            skill.getAttribute("PeriodicidadPago"),
                                            skill.getAttribute("Puesto"),
                                            skill.getAttribute("RiesgoPuesto"),
                                            skill.getAttribute("SalarioBaseCotApor"),
                                            skill.getAttribute("SalarioDiarioIntegrado"),
                                            skill.getAttribute("Sindicalizado"),
                                            skill.getAttribute("TipoContrato"),
                                            skill.getAttribute("TipoJornada"),
                                            skill.getAttribute("TipoRegimen"),
                                            str(UUID))

                            cursor.execute(add_NReceptor, data_NReceptor)

                        for skill in NPercepciones:

                            add_NPercepciones = ("insert into conciliacion_npercepciones " 
                                                "(TotalExento, TotalGravado, TotalSueldos, UUIDInt) "
                                                "values (%s, %s, %s, %s)")

                            data_NPercepciones = (skill.getAttribute("TotalExento"),
                                                skill.getAttribute("TotalGravado"),
                                                skill.getAttribute("TotalSueldos"),
                                                str(UUID))

                            cursor.execute(add_NPercepciones, data_NPercepciones)

                        for skill in NPercepcion:

                            add_NPercepcion = ("insert into conciliacion_npercepcion "
                                            "(Clave, Concepto, ImporteExento, ImporteGravado, TipoPercepcion, UUIDInt) "
                                            "values (%s, %s, %s, %s, %s, %s)")

                            data_NPercepcion = (skill.getAttribute("Clave"),
                                                skill.getAttribute("Concepto"),
                                                skill.getAttribute("ImporteExento"),
                                                skill.getAttribute("ImporteGravado"),
                                                skill.getAttribute("TipoPercepcion"),
                                                str(UUID))

                            cursor.execute(add_NPercepcion, data_NPercepcion)

                        for skill in OtroPago:

                            add_OtroPago = ("insert into conciliacion_otropago "
                                            "(Clave, Concepto, Importe, TipoOtroPago, UUIDInt) "
                                            "values (%s, %s, %s, %s, %s)")

                            data_OtroPago = (skill.getAttribute("Clave"),
                                            skill.getAttribute("Concepto"),
                                            skill.getAttribute("Importe"),
                                            skill.getAttribute("TipoOtroPago"),
                                            str(UUID))

                            cursor.execute(add_OtroPago, data_OtroPago)

                        for skill in SubsidioAlEmpleo:

                            add_SubsidioAlEmpleo = ("insert into conciliacion_subsidioalempleo "
                                                    "(SubsidioCausado, UUIDInt) "
                                                    "values (%s, %s)")

                            data_SubsidioAlEmpleo = (skill.getAttribute("SubsidioCausado"),
                                                    str(UUID))

                            cursor.execute(add_SubsidioAlEmpleo, data_SubsidioAlEmpleo)

                        cnx.commit()

                    except:
                        print("Hubo un problema")
                        e = sys.exc_info()
                        print(e)
                        #sleep(5)

                    finally:
                        print("Cierre de cursores y DB")
                        cursor.close()
                        cnx.close()

                print("Ya existe el XML: " + x)
                cursor.close()
                cnx.close()
                        
if __name__ == "__main__":
    main()