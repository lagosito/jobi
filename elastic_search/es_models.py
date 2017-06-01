import hashlib
import abc

from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Keyword, Text, Date, analyzer
from elasticsearch_dsl.field import Completion

from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME
from elastic_search.utils import check_duplicate, DuplicateHashError


trigram = analyzer(
    'trigram',
    tokenizer="standard",
    filter=["standard", "shingle"],
)


class DataHead(DocType):
    inhash = Keyword()
    source = Text()
    link = Text()
    msg = Text()
    location = Text(multi=True, analyzer=trigram)
    interest = Text()
    job_type = Completion()
    role = Completion()
    organisation = Text(multi=True)
    create_time = Date()

    class Meta:
        index = INDEX_NAME

    @staticmethod
    def bulk_create(docs):
        bulk(create_connection(), (d.to_dict(True) for d in docs), chunk_size=10)

    @abc.abstractmethod
    def decode_from(self, value):
        raise NotImplementedError('Please implement this method in class "%s"' % self.__class__.__name__)

    def __init__(self, *args, **kwargs):
        block = {'val': ''}

        def validate(value):
            if type(value) is dict:
                for val in value:
                    value[val] = validate(value[val])
            elif type(value) in (list, tuple):
                for val in value:
                    val = validate(val)
            else:
                foo = self.decode_from(value)
                block['val'] += foo
                return foo

        validate(kwargs)

        kwargs['inhash'] = hashlib.sha512(block['val']).hexdigest()

        if check_duplicate(create_connection(), kwargs['inhash']):
            super(DataHead, self).__init__(*args, **kwargs)
        else:
            raise DuplicateHashError
