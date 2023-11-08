"""Views for recipe APIs"""

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes)
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagsSerializer,
    IngradientSerializer,
    RecipeImageSerializer
)
from core.models import Recipe, Tags, Ingradient


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Coma separated list\
                    of IDs tags to filter recipes',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Coma separated\
                    listof IDs ingredients to filter recipes',
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for Reciape APIs."""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        return [int(string) for string in qs.split(',')]

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tags_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags_ids)
        if ingredients:
            ingredients_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingradient__id__in=ingredients_ids)
        return queryset.filter(user=self.request.user).order_by(
            '-id').distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Return only recipes assigned to user',
            )
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """View for BaseRecipeAttr APIs."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0)))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()


class TagsViewSet(BaseRecipeAttrViewSet):
    """"Views for Tags API."""
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class IngradientViewSet(BaseRecipeAttrViewSet):
    """View for Ingradient APIs."""
    serializer_class = IngradientSerializer
    queryset = Ingradient.objects.all()
