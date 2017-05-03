import traceback

from django.core.management.base import BaseCommand, CommandError

from elastic_search.es_core_config import create_mappings, get_index


def initialize_es():
    get_index()
    create_mappings()


class Command(BaseCommand):
    help = 'Initialize website with ElasticSearch'

    def handle(self, *args, **options):
        try:
            initialize_es()
            self.stdout.write("ElasticSearch initialized without any errors")
        except Exception as e:
            traceback.print_exc()
            raise CommandError(
                "Some problem occurred. Please follow traceback. Message - %s" % e.message
            )
        else:
            self.stdout.write("Website initialized successfully")
