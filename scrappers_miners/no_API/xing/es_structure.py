from elasticsearch_dsl import Text

from elastic_search.es_models import DataHead


class Xing(DataHead):
    job_title = Text()
    career_level = Text()
    industry = Text()
    description = Text()

    def decode_from(self, value):
        return value.decode('utf-8', 'ignore')
