from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()


def elasticsearch_store(index, text):
    doc = {
        'author': 'adel',
        'text': text,
        'timestamp': datetime.now(),
    }
    res = es.index(index=index, doc_type='text', id=1, body=doc)
    print('created = %s' % res['created'])

    res = es.get(index=index, id=1)
    print(res['_source'])


