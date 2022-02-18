from apiflask import APIBlueprint, input, output, abort, doc
from apiflask.schemas import Schema

import src.controllers.auth as auth
import src.controllers.mail as mail
import src.models.auth as models
from ..utils.enums import ControllerStatus

router = APIBlueprint("auth", __name__, "Authentication", url_prefix="/api/auth")


@router.post("/register")
@input(models.RegistrationRequest)
@output(Schema, 201)
@doc(responses={409: "A user with that username and/or e-mail is already registered"})
def create_user(data):
    result = auth.register_user(data)
    if result[0] == ControllerStatus.ALREADY_EXISTS:
        abort(409)

    if result[0] == ControllerStatus.ERROR:
        abort(500, "registration")

    mail_result = mail.send_email("Verify your account", data["email"], "verify.html",
                                  {"username": data["username"], "link": mail.create_mail_link(result[1], "verify")})
    if mail_result == ControllerStatus.ERROR:
        abort(500, "email")

    return ""


@router.post("/login")
@input(models.LoginRequest)
@output(models.LoginResponse)
@doc(responses={401: "Username and/or password combination is incorrect", 403: "Your account hasn't been verified yet"})
def log_in_user(data):
    result = auth.log_in(data)
    if result[0] == ControllerStatus.ERROR:
        abort(500)

    if result[0] == ControllerStatus.WRONG_CREDS:
        abort(401)

    if result[0] == ControllerStatus.NOT_VERIFIED:
        abort(403)

    return {"token": f"Bearer {result[1]}"}


@router.get("/verify/<token>")
@output(Schema)
@doc(responses={
    200: "Account was verified successfully",
    410: "Link has expired and/or its invalid",
    404: "No token was provided"
})
def verify_account(token):
    result = auth.verify_verification_token(token)
    if result == ControllerStatus.INVALID_LINK:
        abort(410)

    if result == ControllerStatus.ERROR:
        abort(500)

    return ""


@router.post("/send")
@input(models.SendEmailRequest)
@output(Schema)
@doc(responses={
    200: "Email address is valid, but only registered email adresses will receive the message"
})
def send_account_email(data):
    # This should probably not be here
    email_subjects_dict = {
        "verify": "Verify your account",
        "forgot": "Password restoration"
    }

    user_data = auth.get_user_document_by_email(data["email"])
    if user_data[0] == ControllerStatus.DOES_NOT_EXISTS:
        return ""

    if user_data[0] == ControllerStatus.ERROR:
        abort(500)

    result = mail.send_email(email_subjects_dict[data["purpose"]], data["email"], f"{data['purpose']}.html", {
        "username": user_data[1]["username"], "link": mail.create_mail_link(str(user_data[1].id), data["purpose"])
    })

    if result == ControllerStatus.ERROR:
        abort(500)

    return ""
