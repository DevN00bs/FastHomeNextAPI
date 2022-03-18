from flask_socketio import Namespace


class ChatNamespace(Namespace):
    def on_connect(self):
        print("Connected!")
