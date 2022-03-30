from apiflask import APIBlueprint, abort, auth_required, doc, input, output

import fast_home_api.controllers.profiles as c
import fast_home_api.models.profiles as m
from ..utils.auth import auth
from ..utils.enums import ControllerStatus

router = APIBlueprint("prof", __name__, "Profiles", url_prefix="/api")


@router.get("/profile")
@output(m.ProfileData, 200)
@doc(
    summary="Get current user's profile - contact"
)
@auth_required(auth)
def get_profile():
    current = c.read_prof(auth.current_user["id"])
    if current[0] == ControllerStatus.ERROR:
        abort(500)

    if current[0] == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    return current[1]


@router.put("/profile")
@input(m.ProfileData)
@output({}, 204)
@doc(summary="Update current user's profile info based on auth")
@auth_required(auth)
def update_profile(data):
    result = c.update_prof(data, auth.current_user["id"])
    if result == ControllerStatus.ERROR:
        abort(500)

    if result == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    return ""
