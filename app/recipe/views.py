"""Views for recipe APIs"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagsSerializer,
    IngradientSerializer
)
from core.models import Recipe, Tags, Ingradient


class RecipeViewSet(viewsets.ModelViewSet):
    """View for Reciape APIs."""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """View for BaseRecipeAttr APIs."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagsViewSet(BaseRecipeAttrViewSet):
    """"Views for Tags API."""
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class IngradientViewSet(BaseRecipeAttrViewSet):
    """View for Ingradient APIs."""
    serializer_class = IngradientSerializer
    queryset = Ingradient.objects.all()
