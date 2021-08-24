import graphene
from django.db import transaction
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from rest_framework import exceptions

from ingredients.models import Ingredient, Category
from ingredients.serializer import CreateIngredientSerializer
from util.common import get_real_id
from util.errors import ErrorCreate, ErrorUpdate, ErrorDelete


class CreateIngredientWithSerializer(SerializerMutation):
    class Meta:
        serializer_class = CreateIngredientSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class CategoryTypeMutation(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name",)
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        return id


class IngredientTypeMutation(DjangoObjectType):
    category = graphene.Field(CategoryTypeMutation)

    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        return id


class CreateIngredientWithMutation(graphene.Mutation):
    class Arguments:
        # The input arguments
        id = graphene.ID()
        name = graphene.String(required=True)
        notes = graphene.String(required=False)
        category_id = graphene.Int(required=True)

    # define the response of the mutation
    ingredient = graphene.Field(IngredientTypeMutation)

    @staticmethod
    def validate_ingredient(**kwargs):
        category_id = kwargs.get('category_id', None)
        if not Category.objects.filter(id=category_id).exists():
            raise exceptions.NotFound(detail="Not found category")
        return True

    @classmethod
    def mutate(cls, root, info, **kwargs):
        name = kwargs.get('name', None)
        notes = kwargs.get('notes', None)
        category_id = kwargs.get('category_id', None)

        if cls.validate_ingredient(**kwargs):
            try:
                with transaction.atomic():
                    ingredient = Ingredient.objects.create(
                        name=name,
                        notes=notes,
                        category_id=category_id,
                    )
                    return CreateIngredientWithMutation(ingredient=ingredient)
            except Exception as e:
                raise ErrorCreate


class UpdateIngredientWithMutation(graphene.Mutation):
    class Arguments:
        # The input arguments
        id = graphene.ID()
        name = graphene.String(required=False)
        notes = graphene.String(required=False)
        category_id = graphene.Int(required=False)

    # define the response of the mutation
    ingredient = graphene.Field(IngredientTypeMutation)

    @staticmethod
    def validate_ingredient(instance, **kwargs):
        category_id = kwargs.get('category_id', None)
        if instance.category_id != category_id:
            if not Category.objects.filter(id=category_id).exists():
                raise exceptions.NotFound(detail="Not found category")
        return True

    @classmethod
    def mutate(cls, root, info, **kwargs):
        pk = kwargs.get('id', None)
        name = kwargs.get('name', None)
        notes = kwargs.get('notes', None)
        category_id = kwargs.get('category_id', None)

        try:
            _, _id = get_real_id(pk)
            ingredient = Ingredient.objects.select_for_update().get(id=_id, is_deleted=False)
        except Ingredient.DoesNotExist:
            raise exceptions.NotFound

        if cls.validate_ingredient(ingredient, **kwargs):
            try:
                with transaction.atomic():
                    ingredient.category_id = category_id
                    ingredient.name = name
                    ingredient.notes = notes
                    ingredient.save()
                return UpdateIngredientWithMutation(ingredient=ingredient)
            except Exception as e:
                raise ErrorUpdate


class DeleteIngredientWithMutation(graphene.Mutation):
    class Arguments:
        # The input arguments
        id = graphene.ID()

    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        pk = kwargs.get('id', None)

        try:
            _, _id = get_real_id(pk)
            ingredient = Ingredient.objects.select_for_update().get(id=_id, is_deleted=False)
        except Ingredient.DoesNotExist:
            raise exceptions.NotFound

        try:
            with transaction.atomic():
                ingredient.is_deleted = True
                ingredient.save()
            return DeleteIngredientWithMutation(message="Delete success")
        except Exception as e:
            raise ErrorDelete


class IngredientMutations(graphene.ObjectType):
    # Base mutations
    create_ingredient_with_mutation = CreateIngredientWithMutation.Field()
    update_ingredient_with_mutation = UpdateIngredientWithMutation.Field()
    delete_ingredient_with_mutation = DeleteIngredientWithMutation.Field()
