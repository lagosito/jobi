import traceback
import os

from polyglot.downloader import downloader
from polyglot.mapping import Embedding
from polyglot.text import Text
from admin_custom.models import ActivityLog
from scrappers_miners.utils.settings import *


def download_polyglot_libs():
    downloader.download("LANG:en", download_dir=DOWNLOAD_DIR)


def create_list_file():
    try:  # FIXME: check following line dirs and shit
        embeddings = Embedding.load(os.path.join(DOWNLOAD_DIR, "/embeddings2/en/embeddings_pkl.tar.bz2"))
    except Exception as e:
        ActivityLog.objects.create_log(
            None, level='C', view_name='scrappers_miners.utils.utils.create_list_file',
            message='Error in loading library (polyglot) - %s' % e.message,
            traceback=traceback.format_exc()
        )
        return False
    else:

        neighbors = []

        for word in FILTER_LIST_WORDS:
            try:
                neighbors += embeddings.nearest_neighbors(word, top_k=NEAREST_NEIGHBORS)
            except Exception as e:
                ActivityLog.objects.create_log(
                    None, level='W', view_name='scrappers_miners.utils.utils.create_list_file',
                    message='Error in finding neighbors of a word in FILTER_LIST_WORDS with a message - %s' % e.message,
                    traceback=traceback.format_exc()
                )

        filter_words_file = open(FILTER_WORD_FILE_PATH, 'w')

        for n in set(neighbors + FILTER_LIST_WORDS):
            filter_words_file.write(n + '\n')

        filter_words_file.close()

        return True


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
        self.sen = Text(context)

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
