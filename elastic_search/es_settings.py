# Elastic Search global settings
# https://elasticsearch-dsl.readthedocs.io/en/latest/configuration.html
# http://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch


# TODO: complete implementation - future
DATABASE_CONNECTION_INFO = {
    'hosts': ['localhost'],
    'PORT': None,
    'timeout': 100
}

# TODO: complete implementation - future [shards][], etc
INDEX_SETTINGS = {

}

INDEX_NAME = 'jobi'

SCRAPPER_FOLDER_STRUCTURE = {
    'A': 'scrappers_miners.API_struct_data',
    'S': 'scrappers_miners.API_unstruct_data',
    'C': 'scrappers_miners.no_API'
}
