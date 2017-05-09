import traceback

from django.core.management.base import BaseCommand, CommandError

from data.tasks import run_all


def force_update():
    run_all()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            self.stdout.write("Data Mining instantiated.")
            force_update()
        except Exception as e:
            traceback.print_exc()
            raise CommandError(
                "Some problem occurred. Please follow traceback. Message - %s" % e.message
            )
        else:
            self.stdout.write("ElasticSearch Database will be updated shortly. Track using Activity Log.")
