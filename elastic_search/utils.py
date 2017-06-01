from elastic_search.es_settings import INDEX_NAME


class DuplicateHashError(Exception):
    message = "Duplicate hash detected in ElasticSearch DB. Hash already exists."


class DuplicateDataError(Exception):
    message = "Duplicate data block detected in ElasticSearch DB due to repetitive Hash collisions."


class IllegalCollisionLimitError(Exception):
    message = "Set Collision Limit greater than or equal to CHUNK_SIZE, to avoid losing data on script restart/resume."


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
