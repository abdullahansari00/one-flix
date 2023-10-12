from core.views import LoginAPIView, RegisterAPIView, RequestCountView, ResetRequestCountView
from django.urls import path

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("request-count/", RequestCountView.as_view(), name="request_count"),
    path("request-count/reset/", ResetRequestCountView.as_view(), name="reset_request_count"),
]
