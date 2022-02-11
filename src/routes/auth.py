from apiflask import APIBlueprint, input, output, abort
from apiflask.schemas import Schema

from ..controllers.auth import register_user
from ..models.auth import RegistrationRequest

router = APIBlueprint("auth", __name__, "Authentication", url_prefix="/api/auth")


@router.post("/register")
@input(RegistrationRequest)
@output(Schema, 201)
def create_user(data):
    result = register_user(data)
    if not result:
        abort(500)

    return ""
