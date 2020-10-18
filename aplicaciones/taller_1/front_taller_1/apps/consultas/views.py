import os
from http.client import HTTPConnection

import paramiko
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


def EjecutarRA2(request):
    return EjecutarReto("", "config/ra2.txt")


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
        objLocalFilePath = objConfig[6]
        objResultFile = os.path.join(objResultFilePath, objResultFileName)
        objLocalFile = os.path.join(objLocalFilePath, objResultFileName)
        objHadoopResultFile = os.path.join(objHadoopTarget, objResultFileName)

        RunCmd("hadoop fs -get {0} {1}".format(objHadoopResultFile, objResultFilePath))
        DownloadFile(objResultFile, objLocalFile)

        objArchivo = open(objLocalFile, "r")
        objResult = objArchivo.read()
    except OSError as err:
        objResult = "IN_PROCESS"
        # objResult = "OS error: {0}".format(err)
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
        objLocalFilePath = objConfig[6]
        objResultFile = os.path.join(objResultFilePath, objResultFileName)
        objLocalFile = os.path.join(objLocalFilePath, objResultFileName)

        if not os.path.isdir(objLocalFilePath):
            os.mkdir(objLocalFilePath)

        if os.path.isfile(objLocalFile):
            os.remove(objLocalFile)

        RunCmd("mkdir -p {0}".format(objResultFilePath))
        RunCmd("rm {0}".format(objResultFile))
        RunCmd("hadoop fs -rm -r {0}".format(objHadoopTarget))
        RunCmd("hadoop jar {0} {1} {2} {3} {4}".format(
            objJarJobPath,
            objJarJobName,
            objHadoopSource,
            objHadoopTarget,
            objParams))

        objResult = "OK"
    except OSError as err:
        objResult = "OS error: {0}".format(err)

    return HttpResponse(objResult)


def RunCmd(objCommand):
    host_proxy = "connect2.virtual.uniandes.edu.co"
    port_proxy = 443
    host_server = "bigdata-cluster1-ambari.virtual.uniandes.edu.co"
    port_server = 22
    user_server = "bigdata09"
    pass_server = "Rojo2020"

    http_con = HTTPConnection(host_proxy, port_proxy)
    http_con.set_tunnel(host_server, port_server)
    http_con.connect()
    sock = http_con.sock
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host_server, username=user_server, password=pass_server, sock=sock)
    ssh.exec_command(objCommand)

    ssh.close()
    http_con.close()


def DownloadFile(objRemoteFile, objLocalFile):
    host_proxy = "connect2.virtual.uniandes.edu.co"
    port_proxy = 443
    host_server = "bigdata-cluster1-ambari.virtual.uniandes.edu.co"
    port_server = 22
    user_server = "bigdata09"
    pass_server = "Rojo2020"

    http_con = HTTPConnection(host_proxy, port_proxy)
    http_con.set_tunnel(host_server, port_server)
    http_con.connect()
    sock = http_con.sock
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host_server, username=user_server, password=pass_server, sock=sock)
    sftp = ssh.open_sftp()
    sftp.get(objRemoteFile, objLocalFile)

    sftp.close()
    ssh.close()
    http_con.close()
