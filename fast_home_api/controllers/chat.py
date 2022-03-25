from typing import Any, Type

from marshmallow import Schema, ValidationError
from mongoengine.errors import DoesNotExist

from ..models.auth import User
from ..models.chat import ChatEventResponse, ChatEvent, StartConversationResponse
from ..models.properties import PropertyDoc
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


def check_if_is_owner(user_id: str, property_id: str) -> tuple[ControllerStatus, bool]:
    try:
        is_owner = str(PropertyDoc.objects.get(id=property_id).owner.id) == user_id
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS, False

    return ControllerStatus.SUCCESS, is_owner


def save_to_event_queue(user_id: str, event_type: ChatEventType, content: str, date: int,
                        from_id: str, property_id: str) -> ControllerStatus:
    try:
        user_doc = User.objects.get(id=user_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS

    user_doc.events_queue.create(event_type=event_type, content=content, date=date, from_id=from_id,
                                 property_id=property_id)
    user_doc.save()
    return ControllerStatus.SUCCESS


def get_event_queue(user_id: str) -> tuple[ControllerStatus, list[dict[str, Any]]]:
    try:
        user_doc = User.objects.get(id=user_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS, []

    return ControllerStatus.SUCCESS, ChatEventResponse().dump(user_doc.events_queue, many=True)


def destroy_event_queue(user_id: str) -> tuple[ControllerStatus, dict[str, list[dict[str, Any]]]]:
    try:
        user_object = User.objects.get(id=user_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS, {}

    connected_users_events = {}
    for uid, events in create_received_events(user_id, user_object.events_queue).items():
        availability = check_user_availability(uid)
        if availability[0] == ControllerStatus.NOT_AVAILABLE:
            u_obj = User.objects.get(id=uid)
            for event in events:
                u_obj.events_queue.create(**event)
            u_obj.save()
        else:
            connected_users_events[availability[1]] = ChatEventResponse().dump(events, many=True)

    user_object.events_queue.delete()
    user_object.save()
    return ControllerStatus.SUCCESS, connected_users_events


def create_received_events(user_id: str, event_list: list[ChatEvent]) -> dict[str, list[dict[str, Any]]]:
    return {event.from_id: [{"event_type": ChatEventType.STATUS_CHANGE, "content": "received", "date": in_event.date,
                             "from_id": user_id, "property_id": in_event.property_id} for in_event in event_list if
                            in_event.from_id == event.from_id] for event in event_list if
            event.event_type == ChatEventType.MESSAGE}


def get_property_owner(prop_id: str) -> tuple[ControllerStatus, dict[str, str]]:
    try:
        prop_result = PropertyDoc.objects.get(id=prop_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS, {}

    return ControllerStatus.SUCCESS, StartConversationResponse().dump(prop_result)


def destroy_user_session(sid: str) -> ControllerStatus:
    del id_session_dict[list(id_session_dict.keys())[list(id_session_dict.values()).index(sid)]]
    return ControllerStatus.SUCCESS
