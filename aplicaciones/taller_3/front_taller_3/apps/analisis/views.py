import pymongo
import simplejson
from bson import Code
from django.http import HttpResponse
from django.shortcuts import render

MONGODB_HOST = 'localhost'
MONGODB_PORT = '27017'
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"


def Inicio(request):
    return render(request, "views/inicio.html")


def CountLocation(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    users = db["users"]

    mapper = Code("""
        function () {
            emit(this.location, 1);
        }
    """)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    users.map_reduce(mapper, reducer, "result_location")
    result = db.result_location.find()
    client.close()
    return HttpResponse(result)
