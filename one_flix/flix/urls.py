from django.urls import path
from flix.views import CollectionDetailView, CollectionView, MovieListView

urlpatterns = [
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("collection/", CollectionView.as_view(), name="collection"),
    path(
        "collection/<uuid:collection_uuid>/",
        CollectionDetailView.as_view(),
        name="collection_detail",
    ),
]
