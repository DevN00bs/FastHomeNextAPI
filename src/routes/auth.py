from apiflask import APIBlueprint, input, output, abort, doc
from apiflask.schemas import Schema

from ..controllers.auth import register_user
from ..models.auth import RegistrationRequest
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
