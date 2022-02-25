from apiflask import APIBlueprint, input, output, abort, doc, auth_required
from flask import send_file

import src.controllers.properties as c
import src.controllers.upload as p
import src.models.properties as m
from ..utils.auth import auth
from ..utils.enums import ControllerStatus

router = APIBlueprint("prop", __name__, "Properties", url_prefix="/api")


@router.post("/property")
@input(m.NewProperty)
@output(m.NewPropertyResponse, 201)
@doc(summary='Register properties data')
@auth_required(auth)
def create_property(data):
    result = c.register_prop(data, auth.current_user["id"])
    if result[0] == ControllerStatus.ERROR:
        abort(500)

    return {"id": result[1]}


@router.get("/properties")
@output(m.BasicPropertyRead(many=True), 200)
@doc(summary='Get properties info')
def read_property():
    result = c.all_props()
    if result[0] == ControllerStatus.ERROR:
        abort(500)
    return result[1]


@router.put("/property")
@input(m.PropertyUpdate)
@output({}, 204)
@doc(summary="Update properties based on their ID")
@auth_required(auth)
def update_property(data):
    result = c.update_prop(data, auth.current_user["id"])
    if result == ControllerStatus.ERROR:
        abort(500)

    if result == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    if result == ControllerStatus.UNAUTHORIZED:
        abort(403)

    return ""


@router.delete("/property")
@input(m.PropertyDelete)
@output({}, 204)
@doc(summary="Delete properties based on their ID")
@auth_required(auth)
def delete_property(data):
    result = c.delete_prop(data, auth.current_user["id"])
    if result == ControllerStatus.ERROR:
        abort(500)

    if result == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    if result == ControllerStatus.UNAUTHORIZED:
        abort(403)
    return ""


@router.post("/property/photos")
@input(m.UploadPhotosRequest)
@input(m.UploadPhotosQueryRequest, location="form")
@input(m.UploadPhotosFilesRequest, location="files")
@output({}, 204)
@auth_required(auth)
# First parameter is the "hack" request, it serves no purpose internally
def upload_property_photos(_, data, files):
    verify_result = p.check_file_type(p.merge_lists(files))
    if verify_result == ControllerStatus.NOT_AN_IMAGE:
        abort(400, "Endpoint only accepts JPG, PNG and WEBP images")

    result = p.upload_properties_photos(data["id"], auth.current_user["id"], p.merge_lists(files))
    if result == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    if result == ControllerStatus.ERROR:
        abort(500)

    if result == ControllerStatus.UNAUTHORIZED:
        abort(403)

    if result == ControllerStatus.NOT_AN_IMAGE:
        abort(400, "Endpoint only accepts JPG, PNG and WEBP images")

    if result == ControllerStatus.ALREADY_EXISTS:
        abort(400, "This property already has photos. Please, use the PUT endpoint (not existant yet, sorry)")

    return ""


@router.get("/property/photo/<id>")
@doc(hide=True)
def get_photo(id):
    result = p.get_photo_from_db(id)
    if result[0] == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    return send_file(result[1], mimetype=f"image/{result[1].format.lower()}")
