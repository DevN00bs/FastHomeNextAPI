from typing import Any, Type

from marshmallow import Schema, ValidationError
from mongoengine.errors import DoesNotExist

from ..models.auth import User
from ..models.chat import ChatEventResponse
from ..utils.auth import verify_token
from ..utils.enums import ControllerStatus, ChatEventType

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
    try:
        user_sid = id_session_dict[to_user_id]
    except KeyError:
        return ControllerStatus.NOT_AVAILABLE, ""

    return ControllerStatus.SUCCESS, user_sid


def save_to_event_queue(user_id: str, event_type: ChatEventType, content: str, date: int) -> ControllerStatus:
    try:
        user_doc = User.objects.get(id=user_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS

    user_doc.events_queue.create(event_type=event_type, content=content, date=date)
    user_doc.save()
    return ControllerStatus.SUCCESS


def get_event_queue(user_id: str) -> tuple[ControllerStatus, list[dict[str, Any]]]:
    try:
        user_doc = User.objects.get(id=user_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS, []

    return ControllerStatus.SUCCESS, ChatEventResponse().dump(user_doc.events_queue, many=True)


def destroy_user_session(sid: str) -> ControllerStatus:
    del id_session_dict[list(id_session_dict.keys())[list(id_session_dict.values()).index(sid)]]
    return ControllerStatus.SUCCESS
