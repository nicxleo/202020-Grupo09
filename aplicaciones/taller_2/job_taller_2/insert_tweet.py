import json
import os

import pymongo

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 1000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
db = client["Grupo09"]
tweets = db["tweets"]

objPath = "C:/Users/Esteb/Desktop/tweets"
lstFile = os.listdir(objPath)

for objFile in lstFile:
    try:
        oblFullPath = "{0}/{1}".format(objPath, objFile)
        objOpen = open(oblFullPath, "r", encoding="utf-8")
        objJson = objOpen.read()
        objData = json.loads(objJson)

        objExist = tweets.find({"id": objData["id"]}).count()
        if objExist == 1:
            tweets.insert(objData)
            print("tweets.insert: {0}".format(objData["id"]))
    except ValueError:
        try:
            oblFullPath = "{0}/{1}".format(objPath, objFile)
            objOpen = open(oblFullPath, "r", encoding="utf-8")
            objJson = objOpen.read()
            objJson = "[{0}]".format(objJson.replace("}{", "},{"))
            objData = json.loads(objJson)

            for objSubData in objData:
                objExist = tweets.find({"id": objSubData["id"]}).count()
                if objExist == 0:
                    tweets.insert(objSubData)
                    print("tweets.insert: {0}".format(objData["id"]))
        except ValueError:
            print("An exception occurred in: {0}".format(objFile))

print("OK -- Connected to MongoDB at server %s" % (MONGODB_HOST))
client.close()
