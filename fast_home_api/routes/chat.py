from time import time

from flask import request
from flask_socketio import Namespace, ConnectionRefusedError, emit

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
                                                 valid_data[1]["date"], valid_data[1]["decoded_token"]["id"])
            if queue_result == ControllerStatus.DOES_NOT_EXISTS:
                raise ConnectionRefusedError("User not found")

            return {"status": "sent"}

        emit("receive_message", {"message": valid_data[1]["message"], "from": valid_data[1]["decoded_token"]["id"],
                                 "date": valid_data[1]["date"]}, to=user_status[1])
        return {"status": "received"}

    @staticmethod
    def on_queue_consumed(data):
        user_data = c.authenticate_and_validate(m.ChatEnterRequest, data)
        if user_data[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")

        if user_data[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        result = c.destroy_event_queue(user_data[1]["decoded_token"]["id"])
        if result == ControllerStatus.DOES_NOT_EXISTS:
            raise ConnectionRefusedError("User not found")

    @staticmethod
    def on_disconnect():
        c.destroy_user_session(request.sid)
