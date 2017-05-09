import os

from django.conf import settings

DOWNLOAD_DIR = os.path.join(os.path.dirname(settings.BASE_DIR), 'nlp-libs', 'polyglot_libs')

# To filter scrapping results with relevant content using following words and their nearest [k] neighbors
FILTER_LIST_WORDS = ['jobs', 'employee', 'freelance', 'employment', 'fulltime', 'work', 'parttime', 'placement', 'gig',
                     'incumbency', 'occupation', 'opportunity', 'work', 'development']

NEAREST_NEIGHBORS = 10  # [k]

FILTER_WORD_FILE_PATH = os.path.join(settings.BASE_DIR, 'scrappers_miners', 'utils', 'FilterList.txt')

ACCEPTABLE_KEYWORDS_TYPE = ('NOUN', 'PROPN', 'NUM')  # Noun, Proper noun, Number
