from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SuggestRequestSerializer
from .mock_data import RECIPES
from .services import suggest_recipes


class SuggestRecipesView(APIView):
    def post(self, request):
        serializer = SuggestRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ingredients = serializer.validated_data["ingredients"]
        results = suggest_recipes(ingredients, RECIPES)

        return Response({
            "count": len(results),
            "recipes": results
        }, status=status.HTTP_200_OK)
# Create your views here.
