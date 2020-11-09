from weka.classifiers import Classifier
from weka.core.converters import Loader
from weka.core.database import InstanceQuery
import weka.core.jvm as jvm
from weka.core.stemmers import Stemmer
from weka.core.stopwords import Stopwords
from weka.core.tokenizers import Tokenizer
from weka.filters import StringToWordVector, Filter

try:
    jvm.start(class_path=["C:/Users/Esteb/Desktop/db/mongodb_unityjdbc_full.jar"])
    iquery = InstanceQuery()
    iquery.db_url = "jdbc:mongo://localhost:27017/Grupo09"
    iquery.query = "select text from tweets;"
    data = iquery.retrieve_instances()

    #data.attribute_by_name('text').values =

    print(data)

    loader = Loader(classname="weka.core.converters.ArffLoader")
    iris_inc = loader.load_file("C:/Users/Esteb/Desktop/prueba.arff")
    iris_inc.class_is_last()

    #nom2str = Filter(classname=("weka.filters.unsupervised.attribute.StringToNominal"), options=["-R", "2-last"])
    #nom2str.inputformat(data)
    #filtered1 = nom2str.filter(data)

    stemmer = Stemmer(classname="weka.core.stemmers.IteratedLovinsStemmer")
    stopwords = Stopwords(classname="weka.core.stopwords.Rainbow")
    tokenizer = Tokenizer(classname="weka.core.tokenizers.WordTokenizer")
    s2wv = StringToWordVector(options=["-W", "10", "-L", "-C"])
    s2wv.stemmer = stemmer
    s2wv.stopwords = stopwords
    s2wv.tokenizer = tokenizer
    s2wv.inputformat(iris_inc)
    filtered = s2wv.filter(iris_inc)

    print(filtered)

    cls = Classifier(classname="weka.classifiers.bayes.NaiveBayes")
    # cls.build_classifier(filtered1)

    # print(cls)
except ValueError:
    print("An exception occurred" + ValueError)