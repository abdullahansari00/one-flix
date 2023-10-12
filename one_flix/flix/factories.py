import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from flix.models import Collection, Movie


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")


class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Faker("sentence")
    description = factory.Faker("text")
    genres = factory.Faker("word")
    uuid = factory.Faker("uuid4")


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Faker("sentence")
    description = factory.Faker("text")
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def movies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for movie in extracted:
                self.movies.add(movie)
        else:
            for _ in range(3):
                self.movies.add(MovieFactory())
