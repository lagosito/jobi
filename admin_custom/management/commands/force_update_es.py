import traceback

from django.core.management.base import BaseCommand, CommandError

from elastic_search.es_core_config import update_mappings


def force_update():
    update_mappings()


class Command(BaseCommand):
    help = 'Avoid forcefully updating ElasticSearch as it will not handle deletions in mappings/doc_types'

    def handle(self, *args, **options):
        try:
            force_update()
        except Exception as e:
            traceback.print_exc()
            raise CommandError(
                "Some problem occurred. Please follow traceback. Message - %s" % e.message
            )
        else:
            self.stdout.write("ElasticSearch Index Mappings updated. No deletions made.")
