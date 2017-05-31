from elasticsearch.client import Elasticsearch
from elasticsearch_dsl.query import Q
from elasticsearch_dsl.search import Search
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME


def search_view(request):
    print request.GET
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
    end = int(request.GET.get('end', 10000))

    if not (0 > start > end):
        return Response("Illegal Arguments", status=400)

    role = request.GET.get('role', "")
    location = request.GET.get('location', "")
    job_type = request.GET.get('job_type', "")
    when = request.GET.get('when', 0)

    query_string = " ".join([role, location, job_type])

    client = Elasticsearch()
    s = Search(using=client, index=INDEX_NAME)
    q = Q("multi_match", query=query_string, fields=['_all'])
    s = s.query(q).filter("range", **{'create_time': {'gte': when}}).sort('-create_time')[start:end]

    response = s.execute()
    return Response(response.to_dict())


@api_view(['GET'])
def suggestions(request):
    role = request.GET.get('role', None)
    location = request.GET.get('location', None)
    job_type = request.GET.get('job_type', None)

    if any([role, location, job_type]):
        client = create_connection()
        s = Search(using=client, index=INDEX_NAME)
        if job_type:
            s = s.suggest('job_type_suggestions', job_type, phrase={'field': 'job_type'})
        if role:
            s = s.suggest('role_suggestions', job_type, phrase={'field': 'role'})
        if location:
            s = s.suggest('location_suggestions', job_type, phrase={'field': 'location'})
        return JsonResponse(s.execute().to_dict())
    else:
        return JsonResponse({"status": "No data."}, status=status.HTTP_400_BAD_REQUEST)
