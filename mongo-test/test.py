import pymongo

client = pymongo.MongoClient("#mongodbcredentials", 27017, tls=True, tlsAllowInvalidCertificates=True)
db = client.app
collection = db['test']

collection.create_index([('name', 'text')])
docs = collection.find({"$text":{'$search': 'move character'}})


for d in docs:
    print(d)