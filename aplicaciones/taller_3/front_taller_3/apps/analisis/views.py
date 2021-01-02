import pymongo
import simplejson
import re
from bson import Code
from django.http import HttpResponse
from django.shortcuts import render

MONGODB_HOST = 'localhost'
MONGODB_PORT = '27017'
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"


def Inicio(request):
    return render(request, "views/inicio.html")


def ResumenQuestions(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    questions = db["questions"]

    count = questions.count()
    client.close()
    return render(request, "views/resumen_questions.html", context={"count": count})


def ResumenAnswers(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    answers = db["answers"]

    count = answers.count()
    client.close()
    return render(request, "views/resumen_answers.html", context={"count": count})


def ResumenUsers(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    users = db["users"]

    count = users.count()
    client.close()
    return render(request, "views/resumen_users.html", context={"count": count})


def ResumenEntities(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    entities = db["entities"]

    count = entities.count()
    client.close()
    return render(request, "views/resumen_entities.html", context={"count": count})


def ResumenEntitiesQuestions(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    result_entity_questions = db["result_entity_questions"]

    count = 0
    for item in result_entity_questions.find():
        count += int(item["value"])

    client.close()
    return render(request, "views/resumen_merge.html", context={"count": count})


def CountAnswer(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    answers = db["answers"]

    mapper = Code("""
        function () {
            emit(this.question_id, 1);
        }
    """)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    answers.map_reduce(mapper, reducer, "result_answers")
    result = db.result_answers.find().sort("value", pymongo.DESCENDING).limit(50)
    client.close()
    return HttpResponse(result)


def CountLocation(request, json):
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
    result = db.result_location.find({"_id": {"$ne": None}}).sort("value", pymongo.DESCENDING).limit(10)
    client.close()
    return HttpResponse(result)


def CountScore(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    answers = db["answers"]

    mapper = Code("""
        function () {
            emit(this.score, 1);
        }
    """)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    answers.map_reduce(mapper, reducer, "result_score")
    result = db.result_score.find().sort("value", pymongo.DESCENDING).limit(20)
    client.close()
    return HttpResponse(result)


def CountCurrency(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    currency = db["currency"]

    mapper = Code("""
        function () {
            emit(this.currency.value, 1);
        }
    """)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    currency.map_reduce(mapper, reducer, "result_currency")
    result = db.result_currency.find().sort("value", pymongo.DESCENDING).limit(20)
    client.close()
    return HttpResponse(result)


def CountSalaryDollar(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    salary = db["salary"]

    mapper = Code("""
        function () {
            if (this.salary.datatype == "usDollar") {
                emit(this.label.value.replace(/'/i, ""), this.salary.value);
            }
        }
    """)

    reducer = Code("""
        function (key, values) {
            var max = values[0];
            values.forEach(function(val){
                if (val > max) max = val;
            });
            return max;
        }
    """)
    salary.map_reduce(mapper, reducer, "result_salary_dollar")
    result = db.result_salary_dollar.find().sort("value", pymongo.DESCENDING).limit(20)
    client.close()
    return HttpResponse(result)


def CountSalaryEuro(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    salary = db["salary"]

    mapper = Code("""
        function () {
            if (this.salary.datatype == "euro") {
                emit(this.label.value.replace(/'/i, ""), this.salary.value);
            }
        }
    """)

    reducer = Code("""
        function (key, values) {
            var max = values[0];
            values.forEach(function(val){
                if (val > max) max = val;
            });
            return max;
        }
    """)
    salary.map_reduce(mapper, reducer, "result_salary_euro")
    result = db.result_salary_euro.find().sort("value", pymongo.DESCENDING).limit(20)
    client.close()
    return HttpResponse(result)


def CountSalaryPoundSterling(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    salary = db["salary"]

    mapper = Code("""
        function () {
            if (this.salary.datatype == "poundSterling") {
                emit(this.label.value.replace(/'/i, ""), this.salary.value);
            }
        }
    """)

    reducer = Code("""
        function (key, values) {
            var max = values[0];
            values.forEach(function(val){
                if (val > max) max = val;
            });
            return max;
        }
    """)
    salary.map_reduce(mapper, reducer, "result_salary_poundsterling")
    result = db.result_salary_poundsterling.find().sort("value", pymongo.DESCENDING).limit(20)
    client.close()
    return HttpResponse(result)


def CountEmployees(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    employees = db["employees"]

    mapper = Code("""
        function () {
            emit(this.label.value.replace(/'/i, ""), this.numberOfEmployees.value);
        }
    """)

    reducer = Code("""
        function (key, values) {
            var max = values[0];
            values.forEach(function(val){
                if (val > max) max = val;
            });
            return max;
        }
    """)
    employees.map_reduce(mapper, reducer, "result_employees")
    result = db.result_employees.find().sort("value", pymongo.DESCENDING).limit(20)
    client.close()
    return HttpResponse(result)


def CountEntityQuestions(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    questions = db["questions"]
    entities = db["entities"]

    lstentity = ""
    for item in entities.find():
        tag = item["spot"].lower().replace("\n", "")
        tag = re.sub("[{0}]".format(re.escape("\"!@#$%^&*()[]{};:,.<>?|`~-=+")), "", tag)
        lstentity += """"{0}",""".format(tag)
    lstentity = "let entities = [{0}];".format(lstentity.rstrip(","))

    mapper = Code("""
        function () {
            %s
            this.tags.forEach(function(val) {
                if (entities.includes(val)) {
                    emit(val, 1);
                }
            });
        }
    """ % lstentity)

    reducer = Code("""
            function (key, values) {
                return Array.sum(values);
            }
        """)
    questions.map_reduce(mapper, reducer, "result_entity_questions")
    result = db.result_entity_questions.find().sort("value", pymongo.DESCENDING).limit(25)
    client.close()
    return HttpResponse(result)


def CountEntityAnswers(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    answers = db["answers"]
    entities = db["entities"]

    lstentity = ""
    for item in entities.find():
        tag = item["spot"].lower().replace("\n", "")
        tag = re.sub("[{0}]".format(re.escape("\"!@#$%^&*()[]{};:,.<>?|`~-=+")), "", tag)
        lstentity += """"{0}",""".format(tag)
    lstentity = "let entities = [{0}];".format(lstentity.rstrip(","))

    mapper = Code("""
        function () {
            %s
            this.tags.forEach(function(val) {
                if (entities.includes(val)) {
                    emit(val, 1);
                }
            });
        }
    """ % lstentity)

    reducer = Code("""
            function (key, values) {
                return Array.sum(values);
            }
        """)
    answers.map_reduce(mapper, reducer, "result_entity_answers")
    result = db.result_entity_answers.find().sort("value", pymongo.DESCENDING).limit(25)
    client.close()
    return HttpResponse(result)


def CountTagQuestions(request, json):
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    questions = db["questions"]

    mapper = Code("""
        function () {
            this.tags.forEach(function(val) {
                emit(val, 1);
            });
        }
    """)

    reducer = Code("""
        function (key, values) {
            return Array.sum(values);
        }
    """)
    questions.map_reduce(mapper, reducer, "result_tags_questions")
    result = db.result_tags_questions.find().sort("value", pymongo.DESCENDING).limit(120)
    client.close()
    return HttpResponse(result)


def TablaCurrency(request, json):
    lstData = simplejson.loads(json)
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    db = client["Grupo09"]
    currency_name = db["currency_name"]

    result = []
    for item in currency_name.find():
        if item["code"] in lstData:
            result.append(item)

    client.close()
    return render(request, "views/tabla_currency.html", context={"lstResult": result})
