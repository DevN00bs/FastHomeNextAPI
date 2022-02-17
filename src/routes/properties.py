from apiflask import APIBlueprint, input, output, abort, doc
from apiflask.schemas import Schema

from ..controllers.properties import *
from ..models.properties import *
from ..utils.enums import ControllerStatus

router = APIBlueprint("prop", __name__, "Properties", url_prefix="/api")


@router.get('/')
def test():
    return {'message': 'OK'}


@router.post("/property")
@input(NewProperty)
@output(Schema, 201)
@doc(
    summary='Register properties data',
    responses={409: 'A property with that address is already registered'})
def create_property(data):
    result = register_prop(data)
    if result == ControllerStatus.ALREADY_EXISTS:
        abort(409)

    if result == ControllerStatus.ERROR:
        abort(500)

    return ""


@router.get("/properties")
@output(Schema, 200)
@doc(summary='Get properties info')
def read_property():
    result = all_props()
    if result[0] == ControllerStatus.ERROR:
        abort(500)
    return result[1]


@router.put("/property")
@input(PropertyUpdate)
@output(Schema, 200)
@doc(summary="Update properties based on their ID")
def update_property(data):
    result = update_prop(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    return ""


@router.delete("/property")
@input(PropertyDelete)
@output(Schema, 202)
@doc(summary="Delete properties based on their ID")
def delete_property(data):
    result = delete_prop(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    return ""
