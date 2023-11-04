"""Serializers for recipe API"""


from rest_framework import serializers

from core.models import Recipe, Tags


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


class TagsSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tags
        fields = ['id', 'name']
        read_only_fields = ['id']