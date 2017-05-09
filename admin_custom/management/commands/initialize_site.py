import traceback

from django.core.management.base import BaseCommand, CommandError

from elastic_search.es_core_config import create_mappings, get_index
from scrappers_miners.utils.collect import download_polyglot_libs, create_list_file


def initialize_es():
    get_index()
    create_mappings()


def initialize_nlp(marker=False):
    if marker:
        download_polyglot_libs()
    create_list_file()


class Command(BaseCommand):
    help = 'Initialize website with ElasticSearch and NLP toolkit.'

    def add_arguments(self, parser):
        parser.add_argument('--download', action='store_true', dest='download', default=False,
                            help="Download all data/Overwrites existing libs.")

    def handle(self, *args, **options):
        try:
            initialize_es()
            self.stdout.write("ElasticSearch initialized without any errors")
            initialize_nlp(marker=options['download'])
            self.stdout.write("NLP tools initialized without any errors")
        except Exception as e:
            traceback.print_exc()
            raise CommandError(
                "Some problem occurred. Please follow traceback. Message - %s" % e.message
            )
        else:
            self.stdout.write("Website initialized successfully")
