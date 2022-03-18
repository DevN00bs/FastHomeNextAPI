from typing import Any, Type

from marshmallow import Schema, ValidationError

from ..utils.auth import verify_token
from ..utils.enums import ControllerStatus


def authenticate_and_validate(schema: Type[Schema], data: dict[str, Any]) -> tuple[ControllerStatus, dict[str, Any]]:
    valid_result = validate_schema(schema, data)
    if valid_result[0] == ControllerStatus.ERROR:
        return ControllerStatus.ERROR, {}

    verify_result = verify_token(data["token"])
    if not verify_result:
        return ControllerStatus.UNAUTHORIZED, {}

    return ControllerStatus.SUCCESS, {**{field: value for field, value in valid_result[1].items() if field != "token"},
                                      "decoded_token": verify_result}


def validate_schema(schema: Type[Schema], data: dict[str, Any]) -> tuple[ControllerStatus, dict[str, Any]]:
    try:
        return ControllerStatus.SUCCESS, schema().load(data)
    except ValidationError:
        return ControllerStatus.ERROR, {}
