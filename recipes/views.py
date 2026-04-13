from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    SuggestRequestSerializer,
    UserSerializer,
)
from .suggester import get_recipe_suggestions


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user).access_token

        return Response({"access": str(token)}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


class SuggestRecipesView(APIView):
    def post(self, request):
        serializer = SuggestRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ingredients = serializer.validated_data["ingredients"]
        results = get_recipe_suggestions(ingredients)

        return Response({
            "count": len(results),
            "recipes": results
        }, status=status.HTTP_200_OK)
