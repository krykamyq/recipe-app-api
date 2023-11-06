"""Serializers for recipe API"""


from rest_framework import serializers

from core.models import Recipe, Tags, Ingradient


class TagsSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tags
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngradientSerializer(serializers.ModelSerializer):
    """serializer for Ingradient"""
    class Meta:
        model = Ingradient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""
    tags = TagsSerializer(many=True, required=False)
    ingradient = IngradientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price',
            'link', 'tags', 'ingradient']
        read_only_fields = ['id']

    def create(self, validated_data):
        res = validated_data.pop('tags', [])
        res2 = validated_data.pop('ingradient', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in res:
            tag_obj, created = Tags.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)
        for ingredient in res2:
            ingredient_obj, created = Ingradient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingradient.add(ingredient_obj)

        return recipe

    def update(self, instance, validated_data):
        authenticated_user = self.context['request'].user
        if instance.user != authenticated_user:
            raise serializers.ValidationError(
                "You do not havepermission to update this recipe.")

        # Update fields based on validated_data
        for field, value in validated_data.items():
            if field != 'tags' and field != 'ingradient':
                setattr(instance, field, value)

        instance.save()

        # Update the associated tags
        tags_data = validated_data.get('tags', [])
        ingradient_data = validated_data.get('ingradient', [])
        instance.tags.set([])  # Clear existing tags
        instance.ingradient.set([])  # Clear existing ingredients

        for ingredient_data in ingradient_data:
            ingredient, created = Ingradient.objects.get_or_create(
                name=ingredient_data['name'],
                user=instance.user)
            instance.ingradient.add(ingredient)

        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(name=tag_data['name'],
                                                      user=instance.user)
            instance.tags.add(tag)

        return instance


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
