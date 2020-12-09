import pymongo
from SPARQLWrapper import SPARQLWrapper, JSON

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
db = client["Grupo09"]
employees = db["employees"]

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT *
    WHERE
     {
        ?company a dbo:Company;
        dbo:abstract ?abstract;
        rdfs:label ?label;
        dbp:owner ?owner;
        dbo:numberOfEmployees ?numberOfEmployees.
        FILTER(lang(?abstract) = 'en')
        FILTER(lang(?label) = 'en')
     }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
lstresults = results["results"]["bindings"]

for item in lstresults:
    employees.insert(item)

print('---------------------------')

for item in lstresults:
    print('%s: %s' % (item["label"]["xml:lang"], item["label"]["value"]))
