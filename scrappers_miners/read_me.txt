### Guidelines/Rules for building a pluggable scrapper/miner ###

Path to a callable function should be specified in the database under the 'Source' table for executing the
scrapper/miner, which should return data as expected in the specified ElasticSearch structure. The data will be
automatically appended with other relevant information as needed. The code shouldn't rely on any information or module
to be provided by Django, Celery or RabbitMq. It may use independent modules of the same, but should be avoided to
maintain the pluggable behaviour.

Path to the ElasticSearch structure class should be specified in the Database under the same tuple. The stated class
should be a child class of 'elastic_search.es_models.DataHead'. Following are the methods which are expected to be
described under it -
add_method()
