from flask import request
from flask_socketio import Namespace, ConnectionRefusedError, emit

import fast_home_api.controllers.chat as c
import fast_home_api.models.chat as m
from ..utils.enums import ControllerStatus


class ChatNamespace(Namespace):
    @staticmethod
    def on_chat_auth(data):
        valid_data = c.authenticate_and_validate(m.ChatEnterRequest, data)
        if valid_data[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")

        if valid_data[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        c.add_user_to_session(valid_data[1]["decoded_token"]["id"], request.sid)

    @staticmethod
    def on_send_message(data):
        valid_data = c.authenticate_and_validate(m.ChatMessageRequest, data)
        print(valid_data)
        if valid_data[0] == ControllerStatus.ERROR:
            raise ConnectionRefusedError("Invalid request")

        if valid_data[0] == ControllerStatus.UNAUTHORIZED:
            raise ConnectionRefusedError("Invalid credentials")

        user_status = c.check_user_availability(data["to_user_id"])
        if user_status[0] == ControllerStatus.NOT_AVAILABLE:
            return

        emit("receive_message", {"message": valid_data[1]["message"], "from": valid_data[1]["decoded_token"]["id"],
                                 "date": valid_data[1]["date"]}, to=user_status[1])
