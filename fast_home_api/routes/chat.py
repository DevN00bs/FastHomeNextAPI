from flask_socketio import Namespace, ConnectionRefusedError

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
