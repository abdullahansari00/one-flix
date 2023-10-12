from core.models import RequestCount
from django.db import transaction


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with transaction.atomic():
            request_count, _ = RequestCount.objects.select_for_update().get_or_create(
                url=request.path_info
            )
            request_count.count += 1
            request_count.save()

        response = self.get_response(request)
        return response
