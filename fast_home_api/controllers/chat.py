from typing import Any, Type

from marshmallow import Schema, ValidationError

from ..utils.auth import verify_token
from ..utils.enums import ControllerStatus

id_session_dict = {}


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


def add_user_to_session(user_id: str, session_id: str) -> None:
    id_session_dict[user_id] = session_id


def check_user_availability(to_user_id: str) -> tuple[ControllerStatus, str]:
    user_sid = id_session_dict[to_user_id]
    if user_sid is None:
        return ControllerStatus.NOT_AVAILABLE, ""

    return ControllerStatus.SUCCESS, user_sid
