from pydoc import locate

from django.utils import timezone
from celery import group

from data.models import Source
from elastic_search.es_core_config import get_index, get_mapping_class
from elastic_search.es_settings import SCRAPPER_FOLDER_STRUCTURE
from src.celery import app


def validate(source):
    if source.scrapper_active or (source.refresh_rate is 0):
        return False
    else:
        if source.last_finished_at:
            elapsed_time = timezone.now() - source.last_finished_at
            if elapsed_time.total_seconds() > (source.refresh_rate * 3600.00):
                return True
            else:
                return False
        else:
            return True


def update_database(source, data_generator):
    klass = get_mapping_class(source)
    klass.bull_create(data_generator)


@app.task(name='scrapper_handler')
def run_all():
    sources = Source.objects.all()
    group(run_main.s(source.id) for source in sources if validate(source))()


@app.task(name='scrapper')
def run_main(source_id):
    source = Source.objects.get(id=source_id)
    source.scrapper_active = True
    source.save()
    update_database(
        source,
        locate(
            SCRAPPER_FOLDER_STRUCTURE[str(source.ds_type)] + '.' + source.call_method
        )(source.ex_details)
    )
    source.last_finished_at = timezone.now()
    source.counter += 1
    source.scrapper_active = False
    source.save()


@app.task(name='update_ElasticSearch')
def update_es_index(source_id):
    index = get_index()
    source = Source.objects.get(id=source_id)
    klass = get_mapping_class(source)
    if not index.exists_type(doc_type=klass.__name__):
        klass.init()
