import uuid

from django.conf import settings
from flix.models import Collection, Movie
from flix.serializers import CollectionSerializer
from flix.utils import get_movie_list
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class MovieListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        url = request.data.get("url", settings.CREDY_MOVIE_URL)
        data = get_movie_list(url)
        return Response(data, status=status.HTTP_200_OK)


class CollectionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        collections = Collection.objects.filter(user=request.user)
        collections_data = collections.values("uuid", "title", "description")
        genres_list = list(
            collections.exclude(movies__isnull=True)
            .values_list("movies__genres", flat=True)
            .distinct()
        )
        genres = []

        for genre in genres_list:
            genres.extend(genre.split(","))

        genre_counts = {genre: genres.count(genre) for genre in set(genres)}
        top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_genres = [genre[0] for genre in top_genres]

        response_data = {"collections": collections_data, "favourite_genres": ", ".join(top_genres)}

        return Response({"is_success": True, "data": response_data}, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        movies_data = request.data.get("movies")

        if not (title and movies_data):
            raise serializers.ValidationError({"error": "Title and movies are required."})

        collection = self.create_or_update_collection(request, title, description, movies_data)

        return Response({"collection_uuid": collection.uuid}, status=status.HTTP_201_CREATED)

    def create_or_update_collection(self, request, title, description, movies_data):
        collection, _ = Collection.objects.update_or_create(
            title=title, user=request.user, defaults={"description": description}
        )
        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(
                uuid=movie_data.get("uuid", uuid.uuid4()),
                defaults={
                    "title": movie_data.get("title"),
                    "description": movie_data.get("description"),
                    "genres": movie_data.get("genres"),
                },
            )
            collection.movies.add(movie)

        return collection


class CollectionDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, collection_uuid):
        collection = get_object_or_404(Collection, uuid=collection_uuid)
        serializer = CollectionSerializer(collection)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, collection_uuid):
        collection = get_object_or_404(Collection, uuid=collection_uuid)
        title = request.data.get("title")
        description = request.data.get("description")
        movies_data = request.data.get("movies")

        if title:
            collection.title = title
        if description:
            collection.description = description

        if movies_data:
            collection.movies.clear()
            for movie_data in movies_data:
                movie, _ = Movie.objects.get_or_create(
                    uuid=movie_data.get("uuid", uuid.uuid4()),
                    defaults={
                        "title": movie_data.get("title"),
                        "description": movie_data.get("description"),
                        "genres": movie_data.get("genres"),
                    },
                )
                collection.movies.add(movie)

        collection.save()
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, collection_uuid):
        collection = get_object_or_404(Collection, uuid=collection_uuid)

        collection.delete()
        return Response(
            {"message": "Collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
