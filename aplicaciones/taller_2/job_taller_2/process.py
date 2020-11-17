import re
import pymongo
from textblob import TextBlob

MONGODB_HOST = "localhost"
MONGODB_PORT = "27017"
MONGODB_TIMEOUT = 10000
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"


def clean_tweet(tweet):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis


print("###################### Start process #####################")
client = pymongo.MongoClient(URI_CONNECTION, retryWrites=False, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
db = client["Grupo09"]
tweets = db["tweets"]
tags = db["tags"]
hashtags = db["hashtags"]

# lstTweet = tweets.find()
# lstTweet = tweets.find(limit=100)
lstTweet = tweets.find({"subjectivity": None}, limit=100)

for tweet in lstTweet:
    analysis = get_tweet_sentiment(tweet["text"])
    scale = ""

    if analysis.sentiment.polarity > 0.5:
        scale = "excelente"
    elif analysis.sentiment.polarity > 0:
        scale = "bueno"
    elif analysis.sentiment.polarity == 0:
        scale = "neutral"
    elif analysis.sentiment.polarity < -0.5:
        scale = "deficiente"
    elif analysis.sentiment.polarity < 0:
        scale = "malo"

    print("###################### Sentiment #####################")
    tweets.update({"_id": tweet["_id"]}, {"$set":
        {
            "polarity": analysis.sentiment.polarity,
            "scale": scale,
            "subjectivity": analysis.sentiment.subjectivity
        }})

    print("###################### Tags #####################")
    for tag in analysis.tags:
        insert_tag = \
            {
                "tweet_id": tweet["id"],
                "author_id": tweet["author_id"],
                "word": tag[0],
                "tag": tag[1]
            }
        tags.insert(insert_tag)

    print("###################### Hashtags #####################")
    lstHashtag = re.findall(r"#(\w+)", tweet["text"])
    for hashtag in lstHashtag:
        insert_hashtag = \
            {
                "tweet_id": tweet["id"],
                "author_id": tweet["author_id"],
                "hashtag": "#{0}".format(hashtag)
            }
        hashtags.insert(insert_hashtag)

print("OK -- Connected to MongoDB at server %s" % (MONGODB_HOST))
client.close()
print("###################### Finish process #####################")
