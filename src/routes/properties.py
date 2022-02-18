from apiflask import APIBlueprint, input, output, abort, doc
from apiflask.schemas import Schema

import src.controllers.properties as c
import src.models.properties as m
from ..utils.enums import ControllerStatus

router = APIBlueprint("prop", __name__, "Properties", url_prefix="/api")


@router.post("/property")
@input(m.NewProperty)
@output(Schema, 201)
@doc(
    summary='Register properties data',
    responses={409: 'A property with that address is already registered'})
def create_property(data):
    result = c.register_prop(data)
    if result == ControllerStatus.ALREADY_EXISTS:
        abort(409)

    if result == ControllerStatus.ERROR:
        abort(500)

    return ""


@router.get("/properties")
@output(m.PropertyRead(many=True), 200)
@doc(summary='Get properties info')
def read_property():
    result = c.all_props()
    if result[0] == ControllerStatus.ERROR:
        abort(500)
    return result[1]


@router.put("/property")
@input(m.PropertyUpdate)
@output(Schema, 200)
@doc(summary="Update properties based on their ID")
def update_property(data):
    result = c.update_prop(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    return ""


@router.delete("/property")
@input(m.PropertyDelete)
@output(Schema, 200)
@doc(summary="Delete properties based on their ID")
def delete_property(data):
    result = c.delete_prop(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    return ""
