from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import FavoriteRecipe

from .serializers import (
    FavoriteRecipeSerializer,
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


class FavoriteRecipeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteRecipe.objects.filter(user=request.user)
        serializer = FavoriteRecipeSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavoriteRecipeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class FavoriteRecipeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, favorite_id):
        try:
            favorite = FavoriteRecipe.objects.get(
                id=favorite_id,
                user=request.user
            )
        except FavoriteRecipe.DoesNotExist:
            return Response(
                {"detail": "Favorite not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   


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


class FavoriteRecipeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, favorite_id):
        try:
            favorite = FavoriteRecipe.objects.get(id=favorite_id, user=request.user)
        except FavoriteRecipe.DoesNotExist:
            return Response(
                {"detail": "Favorite not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)