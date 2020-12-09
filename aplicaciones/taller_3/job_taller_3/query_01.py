import pymongo
from SPARQLWrapper import SPARQLWrapper, JSON

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
db = client["Grupo09"]
currency = db["currency"]

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT *
    WHERE
     {
        ?country a dbo:Country;
        dbo:abstract ?abstract;
        rdfs:label ?label;
        dbp:currencyCode ?currency.
        FILTER(lang(?abstract) = 'en')
        FILTER(lang(?label) = 'en')
     }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
lstresults = results["results"]["bindings"]

for item in lstresults:
    currency.insert(item)

print('---------------------------')

for item in lstresults:
    print('%s: %s' % (item["label"]["xml:lang"], item["label"]["value"]))
