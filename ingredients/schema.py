import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ingredients.models import Category, Ingredient
from util.common import get_real_id


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        return id


class IngredientsQueries(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    get_ingredient_by_id = graphene.Field(IngredientType, id=graphene.String())

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.select_related("category").filter(is_deleted=False)

    def resolve_get_ingredient_by_id(root, info, **kwargs):
        try:
            _id = kwargs.get('id', None)
            _, _id = get_real_id(_id)
            return Ingredient.objects.get(id=_id, is_deleted=False)
        except Ingredient.DoesNotExist:
            return None
