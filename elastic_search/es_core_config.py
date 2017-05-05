from pydoc import locate

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index
from elasticsearch_dsl import FacetedSearch

from data.models import Source
from es_settings import *


def create_connection():
    return connections.create_connection(**DATABASE_CONNECTION_INFO)


def create_index():
    create_connection()
    db = Index(INDEX_NAME)
    db.settings(**INDEX_SETTINGS)
    db.create()
    return db


def get_index():
    create_connection()
    db = Index(INDEX_NAME)
    if db.exists():
        return db
    else:
        return create_index()


def get_mapping_class(source):
    return locate(
        SCRAPPER_FOLDER_STRUCTURE[str(source.ds_type)] + '.' + source.es_structure
    )


def create_mappings():
    index = get_index()
    for source in Source.objects.all():
        klass = get_mapping_class(source)
        if not index.exists_type(doc_type=klass.__name__):
            klass.init()


# Avoid using following method as ES doesn't handle deletions in a mapping
def update_mappings():
    get_index()
    for source in Source.objects.all():
        klass = get_mapping_class(source)
        klass.init()


class CustomSearch(FacetedSearch):
    index = INDEX_NAME


def search(search_arg):
    return CustomSearch(search_arg).execute()
