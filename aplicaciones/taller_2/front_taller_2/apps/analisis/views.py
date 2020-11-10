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
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    authors = db["authors"]

    lstAuthor = authors.find()
    print('OK -- Connected to MongoDB at server %s' % (MONGODB_HOST))
    client.close()
    return render(request, "views/inicio.html", context={"lstAuthor": lstAuthor})


def TablaTag(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tags = db["tags"]

    lstTag = tags.find({"author_id": objAuthor})
    client.close()
    return render(request, "views/tabla_tags.html", context={"lstTag": lstTag})


def ResumenTweet(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tweets = db["tweets"]

    if objAuthor != "0":
        tweets = tweets.find({"author_id": objAuthor})

    count = tweets.count()
    client.close()
    return render(request, "views/resumen_tweet.html", context={"count": count})


def ResumenWord(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tags = db["tags"]

    if objAuthor != "0":
        tags = tags.find({"author_id": objAuthor})

    count = tags.count()
    client.close()
    return render(request, "views/resumen_word.html", context={"count": count})


def CountScale(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tweets = db["tweets"]

    mapper = Code("""
        function () {
            emit(this.scale, 1);
        }
    """)
    if objAuthor != "0":
        mapper = Code("""
            function () {
                if (this.author_id == % s) emit(this.scale, 1);
            }
        """ % objAuthor)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    tweets.map_reduce(mapper, reducer, "result_scale")
    result = db.result_scale.find()
    client.close()
    return HttpResponse(result)


def CountTag(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tags = db["tags"]

    mapper = Code("""
        function () {
            emit(this.tag, 1);
        }
    """)
    if objAuthor != "0":
        mapper = Code("""
            function () {
                if (this.author_id == % s) emit(this.tag, 1);
            }
        """ % objAuthor)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    tags.map_reduce(mapper, reducer, "result_tags")
    result = db.result_tags.find();
    client.close()
    return HttpResponse(result)


def CountSubjectivity(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tweets = db["tweets"]

    mapper = Code("""
        function () {
            emit(this.subjectivity, 1);
        }
    """)
    if objAuthor != "0":
        mapper = Code("""
            function () {
                if (this.author_id == % s) emit(this.subjectivity, 1);
            }
        """ % objAuthor)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    tweets.map_reduce(mapper, reducer, "result_subjectivity")
    result = db.result_subjectivity.find().sort("_id")
    client.close()
    return HttpResponse(result)


def CountDate(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tweets = db["tweets"]

    mapper = Code("""
        function () {
            emit(this.created_at.substring(0,10), 1);
        }
    """)
    if objAuthor != "0":
        mapper = Code("""
            function () {
                if (this.author_id == % s) emit(this.created_at.substring(0,10), 1);
            }
        """ % objAuthor)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    tweets.map_reduce(mapper, reducer, "result_date")
    result = db.result_date.find().sort("_id")
    client.close()
    return HttpResponse(result)


def CountRetweeted(request, json):
    lstData = simplejson.loads(json)
    objAuthor = lstData["Author"]
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    tweets = db["tweets"]

    mapper = Code("""
        function () {
            if (this.referenced_tweets && this.referenced_tweets.length > 0) {
                emit(this.referenced_tweets[0].type, 1);
            } else {
                emit('regular', 1);
            }
        }
    """)
    if objAuthor != "0":
        mapper = Code("""
            function () {
                if (this.author_id == % s) {
                    if (this.referenced_tweets && this.referenced_tweets.length > 0) {
                        emit(this.referenced_tweets[0].type, 1);
                    } else {
                        emit('regular', 1);
                    }
                }
            }
        """ % objAuthor)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    tweets.map_reduce(mapper, reducer, "result_retweeted")
    result = db.result_retweeted.find().sort("_id")
    client.close()
    return HttpResponse(result)
