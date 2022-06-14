from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo

import tensorflow as tf
import tensorflow_hub as hub
from elasticsearch import Elasticsearch

es = Elasticsearch(
    #elasticsearch credentials
)

graph = tf.Graph()
with tf.compat.v1.Session(graph=graph) as session:
    print("“Downloading pre-trained embeddings from tensorflow hub…”")

    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    text_ph = tf.compat.v1.placeholder(tf.string)

    embeddings = embed(text_ph)

    print("“Done.”")

    print("“Creating tensorflow session…”")

    session = tf.compat.v1.Session()

    session.run(tf.compat.v1.global_variables_initializer())

    session.run(tf.compat.v1.tables_initializer())
    print('Done')

client = pymongo.MongoClient("#mongodbcredentials", 27017, tls=True, tlsAllowInvalidCertificates=True)
db = client.app
collection = db['functions']

app = Flask(__name__)
CORS(app)

def embed_text(text):
    vectors = session.run(embeddings, feed_dict={text_ph: text})

    return [vector.tolist() for vector in vectors]

@app.route('/search', methods=['POST'])
def searchScript():
    response = {}
    body = request.get_json()

    try:
        print(body['query'])
        vector = embed_text([body['query']])

        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'function_vector') + 1.0",
                    "params": {"query_vector": vector[0]}
                }
            }
        }
        result = es.search(index='functions', size= 20, query= script_query, _source={"includes": ["function_name", "function_url"]})
        print(result['hits']['hits'])

        response['result'] = 1
        response['results'] = result['hits']['hits']
    except Exception as e:
        response['result'] = 0
        print(e)

    return jsonify(response)

# @app.route("/search", methods=['POST'])
# def search():
#     response = {}
#     body = request.get_json()

#     query = body['query']

#     try:
#         collection.create_index([('spacedName', 'text')])
#         docs = collection.find({"$text":{'$search': query}})
#         results = list(docs)
#         for i in range(len(results)):
#             results[i]['_id'] = str(results[i]['_id'])

#         response = {
#             'result': 1,
#             'entries': results
#         }
#     except:
#         response = {
#             'result': 0
#         }
#     return jsonify(response)

app.run('0.0.0.0', 5005, True)