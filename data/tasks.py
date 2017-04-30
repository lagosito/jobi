import datetime
from pydoc import locate

from celery import group

from data.models import Source
from src.celery import app

folder_name = {
    'A': 'API_struct_data',
    'S': 'API_unstruct_data',
    'C': 'no_API'
}


def validate(source):
    if source.scrapper_active:
        return False
    else:
        if source.last_finished_at:
            elapsed_time = datetime.datetime.now() - source.last_finish_at
            if elapsed_time.total_seconds() > (source.refresh_rate * 3600.00):
                return True
            else:
                return False
        else:
            return True


def update_database(data):
    print data
    return True


@app.task(name='scrapper_handler')
def run_all():
    sources = Source.objects.all()
    group(run_main.s(source.id) for source in sources if validate(source))()


@app.task(name='scrapper')
def run_main(source_id):
    source = Source.objects.get(id=source_id)
    source.scrapper_active = True
    source.save()
    update_database(locate('data.' + folder_name[source.ds_type] + '.' + source.call_method)(source.ex_details))
    source.last_finished_at = datetime.datetime.now()
    source.counter += 1
    source.scrapper_active = False
    source.save()
