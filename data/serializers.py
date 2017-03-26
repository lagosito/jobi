from rest_framework import serializers

from data.models import Data


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
