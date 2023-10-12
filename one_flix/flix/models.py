import uuid

from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=500)
    description = models.TextField()
    genres = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "movie"
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    movies = models.ManyToManyField(Movie)

    class Meta:
        db_table = "collection"
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        unique_together = [["title", "user"]]

    def __str__(self):
        return self.title
