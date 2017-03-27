# Create your views here.
from rest_framework.generics import ListAPIView

from data.models import Data
from data.serializers import JobSerializer


class JobListing(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        meta = self.kwargs.get('meta')
        return Data.objects.filter_choices(meta)


class AllJobListing(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        return Data.objects.all().order_by('-create_time')[:20]
