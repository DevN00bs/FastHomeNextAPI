from time import time

from flask import request
from flask_socketio import Namespace, ConnectionRefusedError, emit, join_room

import fast_home_api.controllers.chat as c
import fast_home_api.models.chat as m
from ..utils.enums import ControllerStatus, ChatEventType


class ChatNamespace(Namespace):
    @staticmethod
    def on_chat_auth(data):
        valid_data = c.authenticate_and_validate(m.ChatEnterRequest, data)
        if valid_data[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")

        if valid_data[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        c.add_user_to_session(valid_data[1]["decoded_token"]["id"], request.sid)
        emit("user_status_change", {"user_id": valid_data[1]["decoded_token"]["id"], "is_online": True},
             to=valid_data[1]["decoded_token"]["id"], include_self=False)

        queue_result = c.get_event_queue(valid_data[1]["decoded_token"]["id"])
        if queue_result[0] == ControllerStatus.SUCCESS:
            return queue_result[1]

    @staticmethod
    def on_send_message(data):
        data_with_date = {**data, "date": int(round(time() * 1000))}
        valid_data = c.authenticate_and_validate(m.ChatMessageRequest, data_with_date)
        if valid_data[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")

        if valid_data[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        user_status = c.check_user_availability(data["to_user_id"])
        if user_status[0] == ControllerStatus.NOT_AVAILABLE:
            queue_result = c.save_to_event_queue(data["to_user_id"], ChatEventType.MESSAGE, valid_data[1]["message"],
                                                 valid_data[1]["date"], valid_data[1]["decoded_token"]["id"],
                                                 valid_data[1]["property_id"])
            if queue_result == ControllerStatus.DOES_NOT_EXISTS:
                raise ConnectionRefusedError("User not found")

            return {"content": "sent", "date": valid_data[1]["date"]}

        emit("receive_events",
             [{"event_type": ChatEventType.MESSAGE.name, "content": valid_data[1]["message"],
               "from_id": valid_data[1]["decoded_token"]["id"],
               "date": valid_data[1]["date"], "property_id": valid_data[1]["property_id"]}], to=user_status[1])
        return {"content": "received", "date": valid_data[1]["date"]}

    @staticmethod
    def on_queue_consumed(data):
        user_data = c.authenticate_and_validate(m.ChatEnterRequest, data)
        if user_data[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")

        if user_data[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        result = c.destroy_event_queue(user_data[1]["decoded_token"]["id"])
        if result[0] == ControllerStatus.DOES_NOT_EXISTS:
            raise ConnectionRefusedError("User not found")

        for sid, events in result[1].items():
            emit("receive_events", events, to=sid)

    @staticmethod
    def on_start_conversation(data):
        result = c.authenticate_and_validate(m.StartConversationRequest, data)
        if result[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")
        if result[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        owner_id = c.get_property_owner(result[1]["property_id"], result[1]["decoded_token"]["id"])
        if owner_id[0] == ControllerStatus.DOES_NOT_EXISTS:
            raise ConnectionRefusedError("Property not found")

        if "issuer_id" in result[1]:
            issuer_data = c.get_issuer_data(result[1]["issuer_id"])
            if issuer_data[0] == ControllerStatus.DOES_NOT_EXISTS:
                raise ConnectionRefusedError("User not found")

            return owner_id[1] | {"user_id": result[1]["issuer_id"]} | m.IssuerDataResponse().dump(issuer_data[1])

        return owner_id[1]

    @staticmethod
    def on_enter_conversation(data):
        result = c.authenticate_and_validate(m.StartConversationRequest, data)
        if result[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")
        if result[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        if "issuer_id" in result[1]:
            issuer_sid = c.check_user_availability(result[1]["issuer_id"])
            last_seen = c.get_last_seen(result[1]["issuer_id"])
            if last_seen[0] == ControllerStatus.DOES_NOT_EXISTS:
                raise ConnectionRefusedError("User not found")

            join_room(result[1]["issuer_id"])
            return {"is_online": issuer_sid[0] == ControllerStatus.SUCCESS, "last_seen": last_seen[1]}

        prop_data = c.get_property_owner(result[1]["property_id"], result[1]["decoded_token"]["id"])
        if prop_data[0] == ControllerStatus.DOES_NOT_EXISTS:
            raise ConnectionRefusedError("Property not found")

        join_room(prop_data[1]["user_id"])
        return {"is_online": prop_data[1]["is_online"], "last_seen": prop_data[1]["last_seen"]}

    @staticmethod
    def on_user_typing(data):
        result = c.authenticate_and_validate(m.UserTypingRequest, data)
        if result[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")
        if result[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        emit("user_typing", {"user_id": result[1]["decoded_token"]["id"], "is_typing": result[1]["is_typing"]},
             to=result[1]["decoded_token"]["id"],
             include_self=False)

    @staticmethod
    def on_disconnect():
        result = c.get_id_by_session(request.sid)
        if result[0] == ControllerStatus.NOT_AVAILABLE:
            return

        emit("user_status_change", {"user_id": result[1], "is_online": False}, to=result[1], include_self=False)
        c.destroy_user_session(result[1])
