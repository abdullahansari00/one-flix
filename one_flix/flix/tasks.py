from django.conf import settings
from flix.models import Movie
from flix.utils import get_movie_list

from one_flix.celery import app


@app.task(name="populate_movies", max_retries=settings.CREDY_RETRY)
def populate_movies(url=settings.CREDY_MOVIE_URL):
    data = get_movie_list(url)

    if data is None:
        populate_movies.apply_async(args=[url])

    for result in data.get("results"):
        Movie.objects.update_or_create(
            uuid=result["uuid"],
            defaults={
                "title": result["title"],
                "description": result["description"],
                "genres": result["genres"],
            },
        )

    if data.get("next"):
        populate_movies.apply_async(args=[data["next"]])
