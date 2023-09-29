from rest_framework import serializers


class Response201AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False)
    user_id = serializers.IntegerField(required=True)