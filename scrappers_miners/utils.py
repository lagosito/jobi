import os

from polyglot.downloader import downloader
from django.conf import settings

DOWNLOAD_DIR = os.path.join(os.path.dirname(settings.BASE_DIR), 'nlp-libs', 'polyglot_libs')


def download_polyglot_libs():
    downloader.download("LANG:en", download_dir=DOWNLOAD_DIR)


def load_filter_words():
    return []


class NLP(object):
    filter_words = load_filter_words()

    def __init__(self, sen):
        self.sen = sen

    def filter_relevant(self, context):
        pass
