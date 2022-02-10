from apiflask import APIBlueprint, input, output, abort
from apiflask.schemas import Schema
from ..models.auth import RegistrationRequest
from ..controllers.auth import register_user

router = APIBlueprint(name="auth", import_name=__name__)


@router.post("/register")
@input(RegistrationRequest)
@output(Schema, 201)
def create_user(data: RegistrationRequest):
    result = register_user(data)
    if not result:
        abort(500)

    return ""
