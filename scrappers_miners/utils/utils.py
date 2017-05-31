import traceback
import abc

from polyglot.text import Text
from admin_custom.models import ActivityLog
from scrappers_miners.utils.settings import *


def load_filter_words():
    try:
        filter_words_file = open(FILTER_WORD_FILE_PATH)
    except Exception as e:
        ActivityLog.objects.create_log(
            None, level='C', view_name='scrappers_miners.utils.utils.load_filter_words',
            message='Error in finding file containing FILTER_LIST_WORDS with a message - %s' % e.message,
            traceback=traceback.format_exc()
        )
    else:
        return [line.rstrip('\n') for line in filter_words_file.readlines()]


FILTER_WORDS = load_filter_words()


class NLP(object):
    def __init__(self, context, *args, **kwargs):
        self.sen = Text(context, hint_language_code='en')

    def filter_relevant(self):
        tokens = [token for token in self.sen.words if token.lower() in FILTER_WORDS]
        if tokens:
            return True, tokens
        else:
            return False, []

    def get_entities(self):
        di = {}
        for entity in self.sen.entities:
            key = entity.tag.lstrip('I-')
            value = [en for en in entity]
            prev = di.setdefault(key, value)
            di[key] = list(set(prev + value))
        return di

    def get_keywords(self):
        return [word for word, tag in self.sen.pos_tags if tag in ACCEPTABLE_KEYWORDS_TYPE]


class APIHead(object):
    def __init__(self, *args, **kwargs):
        self.ex_details = kwargs.get('ex_details')
        self.data_iterator = None

    @abc.abstractmethod
    def execute(self):
        """
        :returns and sets 'self.data_iterator' to a list of items to be fed in ElasticSearch or a generator for the same.
        """
        raise NotImplementedError('Please implement this method in class "%s"' % self.__class__.__name__)

    def get_ex_details(self):
        return self.ex_details

    def get_data(self):
        if self.data_iterator is not None:
            return self.data_iterator
        else:
            raise NotImplementedError("data_iterator not assigned an iterable object.")
