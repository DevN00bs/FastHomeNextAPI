from apiflask import APIBlueprint, input, output, abort, doc
from apiflask.schemas import Schema

from ..controllers.auth import register_user, log_in
from ..models.auth import RegistrationRequest, LoginRequest, LoginResponse
from ..utils.enums import ControllerStatus

router = APIBlueprint("auth", __name__, "Authentication", url_prefix="/api/auth")


@router.post("/register")
@input(RegistrationRequest)
@output(Schema, 201)
@doc(responses={409: "A user with that username and/or e-mail is already registered"})
def create_user(data):
    result = register_user(data)
    if result == ControllerStatus.ALREADY_EXISTS:
        abort(409)

    if result == ControllerStatus.ERROR:
        abort(500)

    return ""


@router.post("/login")
@input(LoginRequest)
@output(LoginResponse)
@doc(responses={
    401: "Username and/or password combination is incorrect",
    403: "Your account hasn't been verified yet"
})
def log_in_user(data):
    result = log_in(data)
    if result == ControllerStatus.ERROR:
        abort(500)

    if result == ControllerStatus.WRONG_CREDS:
        abort(401)

    if result == ControllerStatus.NOT_VERIFIED:
        abort(403)

    return {"token": "temptoken"}
