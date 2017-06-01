# Elastic Search global settings
# https://elasticsearch-dsl.readthedocs.io/en/latest/configuration.html
# http://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch


DATABASE_CONNECTION_INFO = {
    'hosts': ['localhost'],
    # 'PORT': None,
    # 'timeout': 100
}

INDEX_SETTINGS = {

}

INDEX_NAME = 'jobi'

SCRAPPER_FOLDER_STRUCTURE = {
    'A': 'scrappers_miners.API_struct_data',
    'S': 'scrappers_miners.API_unstruct_data',
    'C': 'scrappers_miners.no_API'
}

CHUNK_SIZE = 10
