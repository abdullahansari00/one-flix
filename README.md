# Movie App

## Contents

- requirements.txt
- development.yml
- OneFlix.postman_collection.json

## Installation

1. Install the dependencies:

    `pip install -r requirements.txt`

2. Run docker:

    `docker-compose -f development.yml up --build --remove-orphans`

3. Set up the database:

    `python manage.py migrate`

4. Set environment variables or hard code them in settings.py.

5. Start the Celery worker:

    `celery -A one_flix worker -l info`

## Tests

- To run the tests, use the following command:

   `python manage.py test`
