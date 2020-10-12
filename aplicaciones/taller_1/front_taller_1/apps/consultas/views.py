import os
from subprocess import call, Popen

import simplejson
from django.http import HttpResponse
from django.shortcuts import render


def Inicio(request):
    lstHora = []
    count = 0
    while count < 24:
        lstHora.append(count)
        count += 1
    return render(request, "views/inicio.html", context={"lstHora": lstHora})


def EjecutarRF1(request, json):
    lstData = simplejson.loads(json)
    objHoraInicio = lstData["HoraInicio"]
    objHoraFin = lstData["HoraFin"]
    objParams = "{0} {1}".format(objHoraInicio, objHoraFin)
    return EjecutarReto(objParams, "config/rf1.txt")


def EjecutarRF2(request, json):
    lstData = simplejson.loads(json)
    objZonaDesde = lstData["ZonaDesde"]
    objZonaHasta = lstData["ZonaHasta"]
    objMes = lstData["Mes"]
    objParams = "{0} {1} {2}".format(objZonaDesde, objZonaHasta, objMes)
    return EjecutarReto(objParams, "config/rf2.txt")


def EjecutarRF3(request, json):
    lstData = simplejson.loads(json)
    objHoraInicio = lstData["HoraInicio"]
    objHoraFin = lstData["HoraFin"]
    objZonaHasta = lstData["ZonaHasta"]
    objParams = "{0} {1} {2}".format(objHoraInicio, objHoraFin, objZonaHasta)
    return EjecutarReto(objParams, "config/rf3.txt")


def ConsultarRespuesta(request, json):
    try:
        lstData = simplejson.loads(json)
        objFileName = lstData["FileName"]
        objFileName = objFileName.replace("-", "/")

        objDirName = os.path.dirname(os.path.realpath("__file__"))
        objFileConfig = open(os.path.join(objDirName, objFileName), "r")
        objConfig = objFileConfig.read().split("\n")

        objResultFileName = objConfig[0]
        objResultFilePath = objConfig[1]
        objHadoopTarget = objConfig[5]
        objResultFile = os.path.join(objResultFilePath, objResultFileName)
        objHadoopResultFile = os.path.join(objHadoopTarget, objResultFileName)

        call("hadoop fs -get {0} {1}".format(objHadoopResultFile, objResultFilePath), shell=True)
        objArchivo = open(objResultFile, "r")
        objResult = objArchivo.read()
    except OSError:
        objResult = "IN_PROCESS"
    return HttpResponse(objResult)


def EjecutarReto(objParams, objFileName):
    try:
        objDirName = os.path.dirname(os.path.realpath("__file__"))
        objFileConfig = open(os.path.join(objDirName, objFileName), "r")
        objConfig = objFileConfig.read().split("\n")

        objResultFileName = objConfig[0]
        objResultFilePath = objConfig[1]
        objJarJobPath = objConfig[2]
        objJarJobName = objConfig[3]
        objHadoopSource = objConfig[4]
        objHadoopTarget = objConfig[5]
        objResultFile = os.path.join(objResultFilePath, objResultFileName)

        if os.path.isfile(objResultFile):
            os.remove(objResultFile)

        call("hadoop fs -rm -r {0}".format(objHadoopTarget), shell=True)
        Popen("hadoop jar {0} {1} {2} {3} {4}".format(objJarJobPath, objJarJobName, objHadoopSource, objHadoopTarget,                                                      objParams), shell=True)

        objResult = "OK"
    except OSError as err:
        objResult = "OS error: {0}".format(err)

    return HttpResponse(objResult)
