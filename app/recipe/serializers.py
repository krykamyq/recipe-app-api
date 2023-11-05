"""Serializers for recipe API"""


from rest_framework import serializers

from core.models import Recipe, Tags


class TagsSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tags
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""
    tags = TagsSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        res = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in res:
            tag_obj, created = Tags.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

        return recipe

    def update(self, instance, validated_data):
        authenticated_user = self.context['request'].user
        if instance.user != authenticated_user:
            raise serializers.ValidationError(
                "You do not havepermission to update this recipe.")

        # Update fields based on validated_data
        for field, value in validated_data.items():
            if field != 'tags':
                setattr(instance, field, value)

        instance.save()

        # Update the associated tags
        tags_data = validated_data.get('tags', [])
        instance.tags.set([])  # Clear existing tags

        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(name=tag_data['name'],
                                                      user=instance.user)
            instance.tags.add(tag)

        return instance


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
