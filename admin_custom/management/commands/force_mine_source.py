import traceback

from django.core.management.base import BaseCommand, CommandError

from data.models import Source
from data.tasks import run_main


def force_mine(source_name):
    run_main(Source.objects.get(name=source_name).id)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source', type=str)

    def handle(self, *args, **options):
        try:
            self.stdout.write("Data Mining instantiated.")
            force_mine(options['source'])
        except Exception as e:
            traceback.print_exc()
            raise CommandError(
                "Some problem occurred. Please follow traceback. Message - %s" % e.message
            )
        else:
            self.stdout.write("Task will be execute shortly. Check Activity Log for errors.")
