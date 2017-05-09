import traceback

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
        tokens = [token for token in self.sen.words() if token in FILTER_WORDS]
        if tokens:
            return True, tokens
        else:
            return False, []

    def get_entities(self):
        return dict((entity.tag.lstrip('I-'), entity) for entity in self.sen.entities)

    def get_keywords(self):
        return [word for word, tag in self.sen.pos_tags if tag in ACCEPTABLE_KEYWORDS_TYPE]
