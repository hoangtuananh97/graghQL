from typing import Union

from graphene import ObjectType
from graphql import GraphQLError
from graphql_relay import from_global_id


def get_real_id(pk: str, only_type: Union[ObjectType, str] = None, raise_error: bool = False):
    try:
        _type, _id = from_global_id(pk) if pk else None
    except (UnicodeDecodeError, ValueError):
        raise GraphQLError(f"Couldn't resolve id: {pk}.")
    if only_type and str(_type) != str(only_type):
        if not raise_error:
            return _type, None
        raise GraphQLError(f"Must receive a {only_type} id.")
    return _type, _id
