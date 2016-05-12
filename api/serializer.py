from rest_framework import serializer

class SearchSerializer(serializers.Serializer):
    pk = serializer.IntegerField()
    image = serializer.ImageField()
    name = serializer.CharField(max_length=100)
