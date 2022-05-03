from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo

client = pymongo.MongoClient("mongodb+srv://cs48000team5:mGTDtJJfQhSVQn4@cluster0.bzb9t.mongodb.net/app?retryWrites=true&w=majority", 27017, tls=True, tlsAllowInvalidCertificates=True)
db = client.app
collection = db['test']

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=['POST'])
def search():
    response = {}
    body = request.get_json()

    query = body['query']

    try:
        collection.create_index([('name', 'text')])
        docs = collection.find({"$text":{'$search': query}})
        results = list(docs)
        for i in range(len(results)):
            results[i]['_id'] = str(results[i]['_id'])

        response = {
            'result': 1,
            'entries': results
        }
    except:
        response = {
            'result': 0
        }
    return jsonify(response)

app.run('0.0.0.0', 5005, True)