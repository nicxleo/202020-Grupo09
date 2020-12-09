import pymongo
import requests
import json
import urllib.parse

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
db = client["Grupo09"]

questions = db["questions"]
entities = db["entities"]
lstquestions = questions.find({"extracted": {"$exists": False}})

for item in lstquestions:
    body = urllib.parse.quote(item["body"])
    apiget = r"https://api.dandelion.eu/datatxt/nex/v1/?lang=en " \
             "&text={0}" \
             "&include=types%2Cabstract%2Ccategories%2Clod" \
             "&token=57e2a085a3a74d02a03bd9dc7303e8e8".format(body)
    response = requests.get(apiget)
    lstentities = json.loads(response.text)
    if lstentities.get("annotations", None) != None:
        questions.update({"question_id": item["question_id"]}, {"$set":
            {
                "extracted": True
            }})
        for entity in lstentities["annotations"]:
            exists = entities.find({"$or": [{"title": entity["title"]}, {"id": entity["id"]}]}).count()
            if exists == 0:
                entities.insert(entity)

client.close()
print("OK -- Connected to MongoDB at server %s" % (MONGODB_HOST))
