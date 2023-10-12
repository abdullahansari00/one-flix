from core.models import RequestCount
from rest_framework import serializers


class RequestCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCount
        fields = ["url", "count"]
