from apiflask import APIBlueprint, abort, auth_required, doc, input, output

import src.controllers.profiles as c
import src.models.profiles as m
from ..utils.auth import auth
from ..utils.enums import ControllerStatus

router = APIBlueprint("prof", __name__, "Profiles", url_prefix="/api")

# Get no endpoint para perfil, dentro de la propiedad *arriba
# Random note over there, just leave it behind


@router.get("/profile")
@output(m.ProfileData(many=True), 200)
@doc(
    summary="Get current user's profile - contact"
    )
@auth_required(auth)
def get_profile():
    current = c.read_prof()
    return current[1]


@router.put("/profile")
@input(m.ProfileUpdate)
@output({}, 204)
@doc(summary="Update current user's profile info based on auth")
@auth_required(auth)
def update_profile(data):
    result = c.update_prof(data, auth.current_user["id"])
    if result == ControllerStatus.ERROR:
        abort(500)

    if result == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    if result == ControllerStatus.UNAUTHORIZED:
        abort(403)

    return ""


'''
@router.delete("/profile")
@input(m.ProfileDelete)
@output({}, 204)
@doc(summary="Delete current user's account - might change then")
@auth_required(auth)
def delete_user(data):
    result = c.delete_prof(data, auth.current_user["id"])
    if result == ControllerStatus.ERROR:
        abort(500)

    if result == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    if result == ControllerStatus.UNAUTHORIZED:
        abort(403)

    return ""
'''
