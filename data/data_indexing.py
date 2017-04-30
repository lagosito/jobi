from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

connections.create_connection()


class Data(DocType):
    source = Text()
    link = Text()
    msg = Text()
    info = 0
    create_time = Date()


def bulk_indexing(data_list):
    Data.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in data_list.iterator()))
