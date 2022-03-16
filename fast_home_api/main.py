from os import environ

from apiflask import APIFlask
from mongoengine import connect
from flask_cors import CORS
from flask_socketio import SocketIO

from .routes.auth import router as auth
from .routes.profiles import router as prof
from .routes.properties import router as prop

app = APIFlask(__name__,
               title="FastHome API",
               version="0.1.0.alpha")
CORS(app)
socket = SocketIO(app)
connect(
    host=environ["DB_HOST"],
    username=environ["DB_USER"],
    password=environ["DB_PASS"],
    db=environ["DB_NAME"]
)


@app.spec_processor
def edit_spec(spec):
    # Remove the actual schemas from the documentation, those won't work
    # The schemas still exist internally because of validation
    # This only affects the OpenAPI schema
    spec["paths"]["/api/property/photos"]["post"]["parameters"] = []
    # Change the content type of the request from "application/json" to "multipart/form-data"
    # It's the only way Swagger UI understands file uploads
    spec["paths"]["/api/property/photos"]["post"]["requestBody"]["content"]["multipart/form-data"] = \
        spec["paths"]["/api/property/photos"]["post"]["requestBody"]["content"][
            "application/json"]
    # Remove the "application/json" content type from the documentation
    del spec["paths"]["/api/property/photos"]["post"]["requestBody"]["content"]["application/json"]
    # Then we mark some parameters as required
    spec["components"]["schemas"]["UploadPhotosRequest"]["required"] = ["property_id", "main_photo"]
    return spec


app.register_blueprint(auth)
app.register_blueprint(prop)
app.register_blueprint(prof)
