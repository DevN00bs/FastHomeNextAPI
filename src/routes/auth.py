from apiflask import APIBlueprint, input, output, abort, doc
from apiflask.schemas import Schema

from ..controllers.auth import register_user, log_in
from ..controllers.mail import send_email, create_verification_link
from ..models.auth import RegistrationRequest, LoginRequest, LoginResponse
from ..utils.enums import ControllerStatus

router = APIBlueprint("auth", __name__, "Authentication", url_prefix="/api/auth")


@router.post("/register")
@input(RegistrationRequest)
@output(Schema, 201)
@doc(responses={409: "A user with that username and/or e-mail is already registered"})
def create_user(data):
    result = register_user(data)
    if result[0] == ControllerStatus.ALREADY_EXISTS:
        abort(409)

    if result[0] == ControllerStatus.ERROR:
        abort(500, "registration")

    mail_result = send_email("Verify your account", data["email"], "verify.html",
                             {"username": data["username"], "link": create_verification_link(result[1])})
    if mail_result == ControllerStatus.ERROR:
        abort(500, "email")

    return ""


@router.post("/login")
@input(LoginRequest)
@output(LoginResponse)
@doc(responses={401: "Username and/or password combination is incorrect", 403: "Your account hasn't been verified yet"})
def log_in_user(data):
    result = log_in(data)
    if result[0] == ControllerStatus.ERROR:
        abort(500)

    if result[0] == ControllerStatus.WRONG_CREDS:
        abort(401)

    if result[0] == ControllerStatus.NOT_VERIFIED:
        abort(403)

    return {"token": f"Bearer {result[1]}"}
