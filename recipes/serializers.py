from rest_framework import serializers


class SuggestRequestSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )