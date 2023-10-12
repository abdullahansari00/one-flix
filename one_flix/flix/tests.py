from django.test import TestCase
from flix.factories import CollectionFactory, MovieFactory, UserFactory
from rest_framework import status
from rest_framework.test import APIClient


class MovieListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_movie_list_success(self):
        response = self.client.get("/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movie_list_invalid_url(self):
        response = self.client.get("/movies/", data={"url": "invalid_url"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movie_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get("/movies/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CollectionViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_collections(self):
        CollectionFactory(user=self.user)
        response = self.client.get("/collection/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_collection_success(self):
        movie1 = MovieFactory()
        movie2 = MovieFactory()
        data = {
            "title": "Test Collection",
            "description": "Test Description",
            "movies": [
                {
                    "title": movie1.title,
                    "description": movie1.description,
                    "genres": movie1.genres,
                    "uuid": str(movie1.uuid),
                },
                {
                    "title": movie2.title,
                    "description": movie2.description,
                    "genres": movie2.genres,
                    "uuid": str(movie2.uuid),
                },
            ],
        }

        response = self.client.post("/collection/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_collection_missing_title(self):
        movie = MovieFactory()
        data = {
            "description": "Test Description",
            "movies": [
                {
                    "title": movie.title,
                    "description": movie.description,
                    "genres": movie.genres,
                    "uuid": str(movie.uuid),
                }
            ],
        }

        response = self.client.post("/collection/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CollectionDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.collection = CollectionFactory(user=self.user)

    def test_get_collection_details_success(self):
        response = self.client.get(f"/collection/{self.collection.uuid}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_collection_details_invalid_uuid(self):
        response = self.client.get(f"/collection/invalid_uuid/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_collection_details(self):
        movie = MovieFactory()
        updated_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "movies": [
                {
                    "title": movie.title,
                    "description": movie.description,
                    "genres": movie.genres,
                    "uuid": str(movie.uuid),
                }
            ],
        }

        response = self.client.put(
            f"/collection/{self.collection.uuid}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_collection(self):
        response = self.client.delete(f"/collection/{self.collection.uuid}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
