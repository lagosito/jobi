import hashlib
import abc

from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Keyword, Text, Date, analyzer
from elasticsearch_dsl.field import Completion

from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME, CHUNK_SIZE
from elastic_search.utils import check_duplicate, DuplicateHashError, DuplicateDataError, IllegalCollisionLimitError

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

    _error_count = 0

    COLLISION_LIMIT = CHUNK_SIZE

    def get_error_count(self):
        return self._error_count

    def set_error_count(self, val):
        self._error_count = val

    error_count = property(get_error_count, set_error_count)

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
            self.error_count += 1
            if self.error_count == self.get_collision_limit():
                self.error_count = 0
                raise DuplicateDataError
            raise DuplicateHashError
