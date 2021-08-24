from django.db import transaction
from rest_framework import serializers

from ingredients.models import Ingredient


class CreateIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    notes = serializers.CharField(max_length=255, required=False)
    category_id = serializers.IntegerField(required=True)

    class Meta:
        model = Ingredient
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return Ingredient.objects.create(
                    name=validated_data['name'],
                    notes=validated_data['notes'],
                    category_id=validated_data['category_id'],
                )
        except Exception as e:
            raise
