from pydoc import locate
import traceback

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index

from admin_custom.models import ActivityLog
from data.models import Source
from es_settings import *


def create_connection():
    try:
        return connections.create_connection(**DATABASE_CONNECTION_INFO)
    except Exception as e:
        ActivityLog.objects.create_log(
            None, level='C', view_name='elastic_search.es_core_config.create_connection',
            message='Error in creating connection with ElasticSearch with error message - %s' % e.message,
            traceback=traceback.format_exc()
        )
        raise Exception(e)


def create_index():
    try:
        create_connection()
        db = Index(INDEX_NAME)
        db.settings(**INDEX_SETTINGS)
        db.create()
    except Exception as e:
        ActivityLog.objects.create_log(
            None, level='C', view_name='elastic_search.es_core_config.create_index',
            message='Error in creating index in ElasticSearch with error message - %s' % e.message,
            traceback=traceback.format_exc()
        )
        raise Exception(e)
    else:
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
        SCRAPPER_FOLDER_STRUCTURE[str(source.ds_type)] + '.' + source.es_structure, forceload=1
    )


def create_mappings():
    client = create_connection()
    index = get_index()
    client.indices.close(index=INDEX_NAME)
    for source in Source.objects.all():
        try:
            klass = get_mapping_class(source)
            if not index.exists_type(doc_type=klass.__name__):
                klass.init()
        except Exception as e:
            ActivityLog.objects.create_log(
                None, entity=source, level='C', view_name='elastic_search.es_core_config.create_mappings',
                message='Error in creating index in ElasticSearch with error message - %s' % e.message,
                traceback=traceback.format_exc()
            )
            raise Exception(e)
    client.indices.open(index=INDEX_NAME)


# Avoid using following method as ES doesn't handle deletions in a mapping
def update_mappings():
    get_index()
    for source in Source.objects.all():
        try:
            klass = get_mapping_class(source)
            klass.init()
        except Exception as e:
            ActivityLog.objects.create_log(
                None, entity=source, level='C', view_name='elastic_search.es_core_config.update_mappings',
                message='Error in updating ElasticSearch with new mappings with error message - %s' % e.message,
                traceback=traceback.format_exc()
            )

    ActivityLog.objects.create_log(
        None, level='W', view_name='data.tasks.update_mappings',
        message='Forced ElasticSearch mapping update.'
    )
