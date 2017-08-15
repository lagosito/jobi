import traceback

from polyglot.downloader import downloader

from polyglot.mapping import Embedding

from admin_custom.models import ActivityLog
from scrappers_miners.utils.settings import *


def download_polyglot_libs():
    downloader.download("LANG:en", download_dir=DOWNLOAD_DIR)


def create_list_file():
    try:
        embeddings = Embedding.load(os.path.join(DOWNLOAD_DIR, "embeddings2/en/embeddings_pkl.tar.bz2"))
    except Exception as e:
        print (e.message)
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
            filter_words_file.write(n.lower() + '\n')

        filter_words_file.close()

        return True
