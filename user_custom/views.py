# FIXME
from django.http.response import JsonResponse

from django.shortcuts import render

# Create your views here.
from elasticsearch.client import Elasticsearch


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
