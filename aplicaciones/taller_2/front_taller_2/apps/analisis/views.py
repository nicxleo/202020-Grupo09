import pymongo
from django.shortcuts import render

MONGODB_HOST = 'localhost'
MONGODB_PORT = '27017'
MONGODB_TIMEOUT = 1000

URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"


def Inicio(request):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    # client.server_info()
    db = client["Grupo09"]
    tweets = db["tweets"]

    query = {"author_id": "126672796"}

    result = tweets.find(query)

    for x in result:
        print(x["text"])

    print('OK -- Connected to MongoDB at server %s' % (MONGODB_HOST))
    client.close()
    return render(request, "views/inicio.html")
