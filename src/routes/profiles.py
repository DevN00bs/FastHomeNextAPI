# Endpoints

from apiflask import APIBlueprint, abort, auth_required, doc, input, output

import src.controllers.profiles as c
import src.models.profiles as m
from ..utils.auth import auth
from ..utils.enums import ControllerStatus

router = APIBlueprint("prof", __name__, "Profiles", url_prefix="/api")

# Minor advances, but structured maybe...
# Current user profile's page - config able
# Same get link cuz just to see info; post for later after admission


@router.get("/user")
@output(m.ProfileConfig(many=False), 200)
@doc(
    summary="Get profiles in general, if current it'll know - editable's other"
    )
# @auth_required(auth)
def current_profile(data):
    result = c.read_profile(data, auth.current_user["id"])
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
