import hashlib

from elasticsearch.helpers import bulk

from elasticsearch_dsl import DocType, Keyword, Text, Date

from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME
from elastic_search.utils import decode_from, check_duplicate, DuplicateHashError

es = create_connection()


class DataHead(DocType):
    inhash = Keyword()
    source = Text()
    link = Text()
    msg = Text()
    location = Text(multi=True)
    interest = Text()
    job_type = Text()
    role = Text()
    organisation = Text(multi=True)
    create_time = Date()

    class Meta:
        index = INDEX_NAME

    @staticmethod
    def bulk_create(docs):
        bulk(create_connection(), (d.to_dict(True) for d in docs))

    def __init__(self, *args, **kwargs):
        enc = kwargs.pop('encoding', 'utf-8')
        block = {'val': ''}

        def validate(value):
            if type(value) is dict:
                for val in value:
                    value[val] = validate(value[val])
            elif type(value) in (list, tuple):
                for val in value:
                    val = validate(val)
            else:
                foo = decode_from(value, enc)
                block['val'] += foo
                return foo

        validate(kwargs)

        kwargs['inhash'] = hashlib.sha512(block['val']).hexdigest()

        if check_duplicate(es, kwargs['inhash']):
            super(DataHead, self).__init__(*args, **kwargs)
        else:
            raise DuplicateHashError
