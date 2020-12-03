import pymongo as pymongo
from stackapi import StackAPI

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

SITE = StackAPI("money")
client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
db = client["Grupo09"]

parameters = db["parameters"]
objpage = parameters.find({"key": "page"})
page = int(objpage[0]["value"])


def insert_owner(db, owner):
    owners = db["owners"]
    if owner.get("user_id", None) is not None:
        exists = owners.find({"user_id": owner["user_id"]}).count()
        if exists == 0:
            insert_obj = \
                {
                    "user_id": owner["user_id"],
                    "sync": False
                }
            owners.insert(insert_obj)


def insert_answer(db, lstanswer):
    for item in lstanswer:
        if item.get("owner", None) is not None:
            insert_owner(db, item["owner"])
            item.setdefault("user_id", item["owner"].get("user_id", None))
            del item["owner"]
        if item.get("comments", None) is not None:
            insert_comment(db, item["comments"])
            del item["comments"]
        answers = db["answers"]
        exists = answers.find({"answer_id": item["answer_id"]}).count()
        if exists == 0:
            answers.insert(item)


def insert_comment(db, lstcomment):
    for item in lstcomment:
        if item.get("owner", None) is not None:
            insert_owner(db, item["owner"])
            item.setdefault("user_id", item["owner"].get("user_id", None))
            del item["owner"]
        comments = db["comments"]
        exists = comments.find({"comment_id": item["comment_id"]}).count()
        if exists == 0:
            comments.insert(item)


def insert_user(db):
    users = db["users"]
    owners = db["owners"]
    lstowner = owners.find({"sync": False})
    lsttmp = []
    tmpuser = ""
    count = 0
    for item in lstowner:
        count += 1
        if count % 100 == 0 or count == lstowner.count():
            tmpuser += "{0};".format(item["user_id"])
            lsttmp.append(tmpuser.rstrip(';'))
            tmpuser = ""
        else:
            tmpuser += "{0};".format(item["user_id"])
    for tmp in lsttmp:
        lstuser = SITE.fetch("users/{0}".format(tmp), filter="!--1nZv)deGu1")
        for item in lstuser.get("items", None):
            exists = users.find({"user_id": item["user_id"]}).count()
            owners.update({"user_id": item["user_id"]}, {"$set":
                {
                    "sync": True
                }})
            if exists == 0:
                users.insert(item)


lstquestions = SITE.fetch("search/advanced", page=page, order="desc", sort="activity",
                          filter="!)awEvQPQkgrHse5fGQeqJIjYI2hOoADCVX7GO9N1uWzfc")
try:
    for item in lstquestions.get("items", None):
        if item.get("owner", None) is not None:
            insert_owner(db, item["owner"])
            item.setdefault("user_id", item["owner"].get("user_id", None))
            del item["owner"]
        if item.get("comments", None) is not None:
            insert_comment(db, item["comments"])
            del item["comments"]
        if item.get("answers", None) is not None:
            insert_answer(db, item["answers"])
            del item["answers"]
        questions = db["questions"]
        exists = questions.find({"question_id": item["question_id"]}).count()
        if exists == 0:
            questions.insert(item)

    insert_user(db)

    if lstquestions.get("has_more", None):
        parameters.update({"key": "page"}, {"$set":
            {
                "value": page + 1
            }})
except ValueError:
    print("An exception occurred in: {0}".format(ValueError))

client.close()
print("OK -- Connected to MongoDB at server %s" % (MONGODB_HOST))
