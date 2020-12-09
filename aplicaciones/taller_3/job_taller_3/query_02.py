from decimal import Decimal

import pymongo
from SPARQLWrapper import SPARQLWrapper, JSON
from bson import Decimal128

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
db = client["Grupo09"]
salary = db["salary"]

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT *
    WHERE
     {
        ?person a dbo:Person;
        dbo:abstract ?abstract;
        rdfs:label ?label;
        dbo:salary ?salary.
        FILTER(lang(?abstract) = 'en')
        FILTER(lang(?label) = 'en')
     }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
lstresults = results["results"]["bindings"]

for item in lstresults:
    value = item["salary"]["value"]
    if "E7" in value:
        value = value.replace("E7", "")
        item["salary"]["value"] = str(Decimal128(str(Decimal(value) * 10000000)))
    if "E8" in value:
        value = value.replace("E8", "")
        item["salary"]["value"] = str(Decimal128(str(Decimal(value) * 100000000)))
    item["salary"]["value"] = str(Decimal128(value))
    item["salary"]["datatype"] = item["salary"]["datatype"].replace("http://dbpedia.org/datatype/", "")
    salary.insert(item)

print('---------------------------')

for item in lstresults:
    print('%s: %s' % (item["label"]["xml:lang"], item["label"]["value"]))
