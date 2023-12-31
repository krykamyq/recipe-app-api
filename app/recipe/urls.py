from rest_framework.routers import DefaultRouter

from django.urls import (
    path,
    include
)

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagsViewSet)
router.register('ingradients', views.IngradientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
