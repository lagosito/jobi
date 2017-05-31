from elastic_search.es_settings import INDEX_NAME


class DuplicateHashError(Exception):
    message = "Duplicate hash detected in ElasticSearch DB. Hash already exists"


def decode_from(value):
    return value.encode('ascii', 'ignore').decode('ascii')


def get_res_count(es, hash_val):
    body = {
        "query": {
            "constant_score": {
                "filter": {
                    "term": {
                        "inhash": hash_val
                    }
                }
            }
        }
    }
    res = es.search(
        index=INDEX_NAME,
        body=body,
    )
    return res['hits']['total']


def check_duplicate(es, hash_val):
    if get_res_count(es, hash_val) == 0:
        return True
    else:
        return False
