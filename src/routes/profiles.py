# Endpoints

from apiflask import APIBlueprint, abort, auth_required, doc, input, output

import src.controllers.profiles as c
import src.models.profiles as m
from ..utils.auth import auth
from ..utils.enums import ControllerStatus

router = APIBlueprint("prof", __name__, "Profiles", url_prefix="/api")

# Both using profileread works?
# Uhh I'm kinda sure I need to understand auth to make this and controller
# Works but so far I advanced these parts


@router.post("/user")
@input(m.ProfileRead)
@output(m.ProfileRead, 200)
@doc(summary="Post to get current user's info in profile")
def current_profile(data):
    return ""


@router.put("/profile")
@input(m.ProfileUpdate)
@output({}, 204)
@doc(summary="Update current user's profile info based on ID and auth")
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
