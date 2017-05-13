from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Date

from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME


class DataHead(DocType):
    source = Text()
    link = Text()
    msg = Text()
    location = Text(multi=True)
    interest = Text()
    job_type = Text()
    organisation = Text(multi=True)
    create_time = Date()

    class Meta:
        index = INDEX_NAME

    @staticmethod
    def bulk_create(docs):
        bulk(create_connection(), (d.to_dict(True) for d in docs))
