from elasticsearch_dsl import Text

from elastic_search.es_models import DataHead


class Xing(DataHead):
    job_title = Text()
    career_level = Text()
    industry = Text()

