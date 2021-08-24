from graphene_federation import build_schema

from ingredients.mutations import IngredientMutations
from ingredients.schema import IngredientsQueries


class Queries(
    IngredientsQueries
):
    pass


class Mutation(
    IngredientMutations
):
    pass


schema = build_schema(Queries, mutation=Mutation)
