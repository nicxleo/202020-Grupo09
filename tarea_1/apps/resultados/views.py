import os
import re
import simplejson
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.resultados.models import Palabra


def Inicio(request):
    lstArchivo = os.listdir("./resources/reuters21578")
    return render(request, 'views/inicio.html', context={'lstArchivo': lstArchivo})


def EjecutarReto(request, json):
    objRespuesta = ''
    lstData = simplejson.loads(json)
    lstArchivos = lstData['NombreArchivo']
    objIdReto = lstData['IdReto']

    lstTotal = []
    for item in lstArchivos:
        objTextoArchivo = open('./resources/reuters21578/' + item, 'r')
        objUpperArchivo = objTextoArchivo.read().upper()
        objTextoNormal = re.sub('[^a-zA-Z \n]', '', objUpperArchivo)
        lstPalabras = objTextoNormal.split()

        objTotal = lstPalabras.__len__()
        lstTotal.append(Palabra(item, objTotal))

        if objIdReto != '4':
            objRespuesta += '#===============================================================#\n'
            objRespuesta += 'Reto para el archivo "' + item + '"\n'
            objRespuesta += '#===============================================================#\n'
            objRespuesta += RetoIndividual(objIdReto, lstPalabras)
            objRespuesta += '\n'
    if objIdReto == '4':
        objMaxTotal = max(lstTotal, key=lambda x: x.cantidad)
        objRespuesta += 'El archivo con más palabras es "' + objMaxTotal.palabra + '" con: ' + str(objMaxTotal.cantidad) + ' palabras\n'
    return HttpResponse(objRespuesta)


def RetoIndividual(objIdReto, lstPalabras):
    objRespuesta = ''
    if objIdReto == '1':
        objTotal = lstPalabras.__len__()
        objRespuesta += 'El total de palabras del archivo es: ' + str(objTotal) + ' palabras\n'
    if objIdReto == '2':
        lstSinRepetir = list(set(lstPalabras))
        lstSinRepetir.sort()
        for item in lstSinRepetir:
            objTotal = lstPalabras.count(item)
            objRespuesta += 'La palabra "' + item + '" aparece: ' + str(objTotal) + ' veces\n'
    if objIdReto == '3':
        lstSinRepetir = list(set(lstPalabras))
        lstSinRepetir.sort()
        lstTotal = []
        for item in lstSinRepetir:
            objTotal = lstPalabras.count(item)
            lstTotal.append(Palabra(item, objTotal))
        lstSorted = sorted(lstTotal, key=lambda x: x.cantidad, reverse=True)
        for item in lstSorted:
            objRespuesta += 'La palabra "' + item.palabra + '" aparece: ' + str(item.cantidad) + ' veces\n'
    return objRespuesta
