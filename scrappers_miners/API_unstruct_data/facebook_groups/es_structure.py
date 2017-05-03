from elasticsearch_dsl import Keyword

from elastic_search.es_models import DataHead


class Facebook(DataHead):
    keywords = Keyword(multi=True)
