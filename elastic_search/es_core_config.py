from pydoc import locate

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index

from data.models import Source
from es_settings import *


# TODO: Complete frame - future [using es_settings.DATABASE_CONNECTION_INFO]
def create_connection():
    return connections.create_connection(hosts=['localhost'])
    # if host is None:
    #     host = ['localhost']
    #
    # else:
    #     if port is None:
    #         pass


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
