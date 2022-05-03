import pymongo

client = pymongo.MongoClient("mongodb+srv://cs48000team5:mGTDtJJfQhSVQn4@cluster0.bzb9t.mongodb.net/app?retryWrites=true&w=majority", 27017, tls=True, tlsAllowInvalidCertificates=True)
db = client.app
collection = db['test']

collection.create_index([('name', 'text')])
docs = collection.find({"$text":{'$search': 'move character'}})


for d in docs:
    print(d)