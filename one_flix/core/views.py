from core.models import RequestCount
from core.serializers import RequestCountSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Both username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"access_token": access_token}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Both username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)


class RequestCountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filter = request.data.get("filter", {})
        exclude = request.data.get("exclude", {})
        request_counts = RequestCount.objects.filter(**filter).exclude(**exclude)
        serializer = RequestCountSerializer(request_counts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetRequestCountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filter = request.data.get("filter", {})
        exclude = request.data.get("exclude", {})
        request_counts = RequestCount.objects.filter(**filter).exclude(**exclude)
        serializer = RequestCountSerializer(request_counts, many=True)
        request_counts.update(count=0)

        return Response(serializer.data, status=status.HTTP_200_OK)
