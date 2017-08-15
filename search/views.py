from elasticsearch.client import Elasticsearch
from elasticsearch_dsl.search import Search
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME


def get_body(role=None, location=None, job_type=None):
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "_all": {
                                "query": role,
                            }
                        }
                    } if role else {},
                    {
                        "match": {
                            "_all": {
                                "query": location,
                            }
                        }
                    } if location else {},
                    {
                        "match": {
                            "_all": {
                                "query": job_type,
                            }
                        }
                    } if job_type else {},
                ]
            },

        }
    }
    return body


def search_view(request):
    print (request.GET)
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')

        es = Elasticsearch()
        res = es.search(index="jobi", body={"query": {"match": {"_all": str(keyword)}}})

        return JsonResponse(res['hits'])
    else:
        return JsonResponse({"status": "KAT GYA"})


@api_view(['GET'])
def recent_jobs_api(request):
    start = int(request.GET.get('start', 0))

    if start < 0:
        return Response("Illegal Arguments", status=400)

    client = Elasticsearch()
    s = Search(using=client, index=INDEX_NAME)
    q = s.query("match_all").sort('-create_time')[start:]
    response = q.execute()

    return Response(response.to_dict())


@api_view(['GET'])
def search_job_api(request):
    start = int(request.GET.get('start', 0))
    end = int(request.GET.get('end', 100))

    if not (0 <= start < end):
        return Response("Illegal Arguments", status=400)

    role = request.GET.get('role', "")
    location = request.GET.get('location', "")
    job_type = request.GET.get('job_type', "")
    when = request.GET.get('when', 0)

    # query_string = " ".join([role, location, job_type])
    #
    # client = Elasticsearch()
    # s = Search(using=client, index=INDEX_NAME)
    # q = Q("multi_match", query=query_string, fields=['_all'])
    # s = s.query(q).filter("range", **{'create_time': {'gte': when}}).sort('-create_time')[start:end]

    es = create_connection()
    res = es.search(
        index=INDEX_NAME,
        body=get_body(role, location, job_type),
        from_=start,
        size=(end - start)
    )

    return Response(res)


@api_view(['GET'])
def suggestions(request):
    role = request.GET.get('role', None)
    location = request.GET.get('location', None)
    job_type = request.GET.get('job_type', None)

    if any([role, location, job_type]):
        client = create_connection()
        s = Search(using=client, index=INDEX_NAME)
        s = s.source(False)
        if job_type:
            s = s.suggest(
                'job_type_suggestions',
                job_type,
                completion={
                    'field': 'job_type.suggester',
                    "fuzzy": {},
                    'size': 20
                }
            )
        if role:
            s = s.suggest(
                'role_suggestions',
                role,
                completion={
                    'field': 'role.suggester',
                    "fuzzy": {},
                    'size': 20
                }
            )
        if location:
            s = s.suggest(
                'location_suggestions',
                location,
                completion={
                    'field': 'location.suggester',
                    "fuzzy": {},
                    'size': 20
                }
            )
        suggestion_res = s.execute().to_dict()['suggest']
        fin_res = {}
        for res in suggestion_res.keys():
            options = []
            for option in suggestion_res[res][0]['options']:
                options.append(option['text'])
            options = list(set(options))
            foo = []
            for val in options:
                foo.append({'value': val, 'data':val})
            fin_res.update({res: foo})
        return Response(fin_res)
    else:
        return Response({"status": "No data."}, status=status.HTTP_400_BAD_REQUEST)
