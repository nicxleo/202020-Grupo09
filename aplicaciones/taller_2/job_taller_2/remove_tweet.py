import pymongo

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

objLoop = True
while objLoop:

    client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tweets = db["tweets"]

    pipeline = [
        {
            u"$group": {
                u"_id": {
                    u"id": u"$id"
                },
                u"count": {
                    u"$sum": 1
                }
            }
        },
        {
            u"$project": {
                u"id": u"$_id.id",
                u"count": u"$count",
                u"_id": 0
            }
        }
    ]

    cursor = tweets.aggregate(
        pipeline,
        allowDiskUse=True
    )

    objLoop = False
    for objTweet in cursor:
        if objTweet["count"] > 1:
            tweets.delete_one({"id": objTweet["id"]})
            print(objTweet)
            objLoop = True

    print("OK -- Connected to MongoDB at server %s" % (MONGODB_HOST))
    client.close()
