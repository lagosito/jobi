from elasticsearch_dsl import Keyword
from elasticsearch_dsl.field import Date, Text, Nested

from elastic_search.es_models import DataHead


class Facebook(DataHead):

    group_detail_list = ['id', 'cover', 'description', 'name']
    post_extra_data = ['id', 'message', 'updated_time', 'permalink_url']

    keywords = Keyword(multi=True)
    group_name = Text()
    post_date = Date()
    extra_data = Nested()
    group_extra_data = Nested(
        properties=dict(map(lambda x: (x, Text()), group_detail_list))
    )
