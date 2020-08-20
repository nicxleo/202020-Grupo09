import os
import simplejson
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def Inicio(request):
    lstArchivo = os.listdir("./resources/reuters21578")
    return render(request, 'views/inicio.html', context={'lstArchivo': lstArchivo})


def EjecutarReto(request, json):
    objRespuesta = ''
    lstData = simplejson.loads(json)
    objNombreArchivo = lstData['NombreArchivo']
    objIdReto = lstData['IdReto']
    objArchivo = open('./resources/reuters21578/' + objNombreArchivo, 'r')
    objTextoArchivo = objArchivo.read()

    if objIdReto == '1':
        objPalabras = objTextoArchivo.split()
        objConteo = objPalabras.__len__()
        objRespuesta = 'El total de palabras del archivo es: ' + str(objConteo)
    return HttpResponse(objRespuesta)
