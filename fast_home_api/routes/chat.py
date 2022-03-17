from flask_socketio import Namespace, emit


class ChatNamespace(Namespace):
    def on_connect(self):
        print("Connected!")
