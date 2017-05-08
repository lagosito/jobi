# FIXME
from django.http.response import JsonResponse

from django.shortcuts import render

# Create your views here.
from elasticsearch.client import Elasticsearch
from elasticsearch_dsl.query import Q
from elasticsearch_dsl.search import Search
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from essentials.serializers import NewsletterSubscriptionSerializer


def main_view(request):

    return render(request, 'main.html', {})


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
    s = Search(using=client, index="jobi")
    q = s.query("match_all").sort('-create_time')[start:]
    response = q.execute()

    return Response(response.to_dict())


@api_view(['GET'])
def search_job_api(request):
    start = int(request.GET.get('start', 0))
    end = int(request.GET.get('end', 10000))

    if start < 0 and end < 0 and end > start:
        return Response("Illegal Arguments", status=400)

    role = request.GET.get('role', "")
    location = request.GET.get('location', "")
    job_type = request.GET.get('job_type', "")
    when = request.GET.get('when', 0)

    query_string = " ".join([role, location, job_type])

    client = Elasticsearch()
    s = Search(using=client, index="jobi")
    q = Q("multi_match", query=query_string, fields=['_all'])
    s = s.query(q).filter("range", **{'create_time': {'gte': when}}).sort('-create_time')[start:end]

    response = s.execute()
    return Response(response.to_dict())


class NewsletterSubscriptionView(APIView):
    def post(self, request, format=None):
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)