from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from sklearn.feature_extraction.text import CountVectorizer
from scipy import spatial

client = pymongo.MongoClient("mongodb+srv://cs48000team5:mGTDtJJfQhSVQn4@cluster0.bzb9t.mongodb.net/app?retryWrites=true&w=majority", 27017, tls=True, tlsAllowInvalidCertificates=True)
db = client.app
collection = db['functions_all']

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=['POST'])
def search():
    response = {}
    body = request.get_json()

    query = body['query']

    try:

        #collection.create_index([('spacedName', 'text')])
        docs = collection.find({})
        results = list(docs)
        sums = []
        for i in range(len(results)):
            if len(results[i]['spacedName']) == 1:
                continue
            results[i]['_id'] = str(results[i]['_id'])

            fileName = results[i]['path'].split('/')
            fileName = fileName[len(fileName) - 1].split('#')[0]
            fileName = fileName.split('.')
            fileName.pop(len(fileName) - 1)
            fileName = '.'.join(fileName)

            vectorizer = CountVectorizer()
            X = vectorizer.fit_transform([query, results[i]['spacedName']])
            simArr = X.toarray()
            result = 1 - spatial.distance.cosine(simArr[0], simArr[1])

            vectorizer2 = CountVectorizer()
            X2 = vectorizer2.fit_transform([query, fileName])
            simArr2 = X2.toarray()
            result2 = 1 - spatial.distance.cosine(simArr2[0], simArr2[1])
            
            result += result2

            if results[i]['spacedName'] == 'Kill Player':
                print(result)
            if result > 0:
                print(fileName)
                sums.append([result, i])
                #print(results[i]['spacedName'])
                # print(result)
            
        # find the element with maximum zeroth element
        sums.sort(key = lambda x: x[0])
        sums.reverse()
        for i in range(len(sums[:30])):
            print(results[sums[i][1]]['spacedName'], sums[i][0], results[sums[i][1]]['path'], sums[i][0])



        response = {
            'result': 1,
            #'entries': results
        }
    except:
        response = {
            'result': 0
        }
    return jsonify(response)

app.run('0.0.0.0', 5005, True)