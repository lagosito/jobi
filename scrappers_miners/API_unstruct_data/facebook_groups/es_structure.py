from elasticsearch_dsl import Keyword
from elasticsearch_dsl.field import Date, Text, Nested

from elastic_search.es_models import DataHead
from scrappers_miners.API_unstruct_data.facebook_groups.API import FacebookGroupCrawler


def get_nested_fields_as_properties():
    return dict(map(lambda x: (x, Text()), FacebookGroupCrawler.get_group_detail_list()))


class Facebook(DataHead):
    keywords = Keyword(multi=True)
    group_name = Text()
    post_date = Date()
    extra_data = Nested()
    group_extra_data = Nested(
        properties=get_nested_fields_as_properties()
    )
