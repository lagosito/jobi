import hashlib
from elasticsearch.helpers import bulk

from elasticsearch_dsl import DocType, Keyword, Text, Date, Completion

from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME, CHUNK_SIZE
from elastic_search.utils import check_duplicate, DuplicateHashError, DuplicateDataError, IllegalCollisionLimitError


class DataHead(DocType):
    inhash = Keyword()
    source = Text()
    link = Text()
    msg = Text()
    location = Text(
        multi=True,
        fields={
            'suggester': Completion(preserve_separators=False)
        }
    )
    interest = Text()
    job_type = Text(
        fields={
            'suggester': Completion(preserve_separators=False)
        }
    )
    role = Text(
        fields={
            'suggester': Completion(preserve_separators=False)
        }
    )
    organisation = Text(multi=True)
    create_time = Date()

    COLLISION_LIMIT = CHUNK_SIZE

    error_count = 0

    class Meta:
        index = INDEX_NAME

    def get_collision_limit(self):
        if self.COLLISION_LIMIT >= CHUNK_SIZE:
            return self.COLLISION_LIMIT
        else:
            raise IllegalCollisionLimitError

    @staticmethod
    def bulk_create(docs):
        bulk(create_connection(), (d.to_dict(True) for d in docs), chunk_size=CHUNK_SIZE)

    @staticmethod
    def _encode_for_hash(value):
        return value.encode('utf-8')

    @staticmethod
    def _decode(value):
        try:
            return unicode(value, 'utf-8', 'ignore')
        except TypeError:
            return value

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
                if value:
                    value = self._decode(value)
                    block['val'] += self._encode_for_hash(value)
                return value

        validate(kwargs)

        kwargs['inhash'] = hashlib.sha512(block['val']).hexdigest()

        if check_duplicate(create_connection(), kwargs['inhash']):
            self.__class__.error_count = 0
            super(DataHead, self).__init__(*args, **kwargs)
        else:
            self.__class__.error_count += 1
            if self.__class__.error_count >= self.get_collision_limit():
                raise DuplicateDataError
            raise DuplicateHashError
