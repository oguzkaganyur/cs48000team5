import tensorflow as tf
import tensorflow_hub as hub
import json
from elasticsearch import Elasticsearch

es = Elasticsearch(
    cloud_id="cs48000:ZXVyb3BlLXdlc3QzLmdjcC5jbG91ZC5lcy5pbyQyYjJkMGQ1NDBhYTU0MjJhYWJkNTRjNjY5OWMxYTdiMiQzMjI2M2I4Njg1MmE0OGNlYjE1Njk2ZmYxNjQwM2M4MA==",
    basic_auth=('elastic', '8cztJbYVnxVKJvxmhws35usN'),
    verify_certs=False, ssl_show_warn=False
)


f = open("C:\\Users\\KAGAN\\Desktop\\functions-all.json")
data = json.load(f)

graph = tf.Graph()

with tf.compat.v1.Session(graph=graph) as session:
    print("“Downloading pre-trained embeddings from tensorflow hub…”")

    embed = hub.load("C:\\Users\\KAGAN\\Desktop\\tf")

    text_ph = tf.compat.v1.placeholder(tf.string)

    embeddings = embed(text_ph)

    print("“Done.”")

    print("“Creating tensorflow session…”")

    session = tf.compat.v1.Session()

    session.run(tf.compat.v1.global_variables_initializer())

    session.run(tf.compat.v1.tables_initializer())

print("“Done.”")


def embed_text(text):
    vectors = session.run(embeddings, feed_dict={text_ph: text})

    return [vector.tolist() for vector in vectors]

text="Start"

for i in data:
    text_vector = embed_text([i['spacedName']])[0]
    es.index(
        index='functions',
        document={
            'function_name': i['name'],
             'function_spaced': i['spacedName'],
             'function_url': i['path'],
             'function_vector': text_vector
        })



#print(embed_text("Start"))


