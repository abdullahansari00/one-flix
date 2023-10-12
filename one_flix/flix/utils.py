import time

import requests
from django.conf import settings


def get_movie_list(url=settings.CREDY_MOVIE_URL):
    auth = (settings.CREDY_USERNAME, settings.CREDY_PASSWORD)

    for _ in range(settings.CREDY_RETRY):
        try:
            response = requests.get(url, auth=auth, verify=False)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

    return None
