import os
from subprocess import call

import simplejson
from django.http import HttpResponse
from django.shortcuts import render


def Inicio(request):
    lstHora = []
    count = 0
    while count < 24:
        lstHora.append(count)
        count += 1
    return render(request, 'views/inicio.html', context={'lstHora': lstHora})


def EjecutarRF1(request, json):

    lstData = simplejson.loads(json)
    objHoraInicio = lstData['HoraInicio']
    objHoraFin = lstData['HoraFin']

    if os.path.isfile('/home/bigdata09/nicolas/respuesta/part-r-00000'):
        os.remove('/home/bigdata09/nicolas/respuesta/part-r-00000')

    call('hadoop fs -rm -r /tmp/bigdata09/result_RF1', shell=True)
    call('hadoop jar /home/bigdata09/nicolas/RF1MR-1.jar uniandes.rf1.mr.JobMR /tmp/bigdata09/datos /tmp/bigdata09/result_RF1 ' + objHoraInicio + ' ' + objHoraFin, shell=True)
    call('hadoop fs -get /tmp/bigdata09/result_RF1/part-r-00000 /home/bigdata09/nicolas/respuesta/', shell=True)

    objArchivo = open('/home/bigdata09/nicolas/respuesta/part-r-00000', 'r')
    objTexto = objArchivo.read()

    return HttpResponse(objTexto)
