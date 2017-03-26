# Create your views here.
from rest_framework.generics import ListAPIView

from data.models import Data
from data.serializers import JobSerializer


class JobListing(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = JobSerializer
