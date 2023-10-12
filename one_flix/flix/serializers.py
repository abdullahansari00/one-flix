from flix.models import Collection, Movie
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["uuid", "title", "description", "genres"]


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ["uuid", "title", "description", "movies"]
