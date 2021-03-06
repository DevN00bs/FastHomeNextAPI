from apiflask import APIBlueprint, input, output, abort, doc, auth_required
from flask import send_file

import fast_home_api.controllers.properties as c
import fast_home_api.controllers.upload as p
import fast_home_api.models.properties as m
import fast_home_api.utils.examples as ex
from ..utils.auth import auth
from ..utils.enums import ControllerStatus

router = APIBlueprint("prop", __name__, "Properties", url_prefix="/api")


@router.post("/property")
@input(m.NewProperty, example=ex.post_property_request_example)
@output(m.NewPropertyResponse, 201, example=ex.post_property_response_example)
@doc(summary='Create a new property and returns its ID',
     description="""Note: After calling this route, you need to upload at least 1 image using the 'photos' route,
     otherwise it won't be considered valid""")
@auth_required(auth)
def create_property(data):
    result = c.register_prop(data, auth.current_user["id"])
    if result[0] == ControllerStatus.ERROR:
        abort(500)

    return {"id": result[1]}


@router.get("/properties")
@input(m.PropertyOptionsRequest, location="query")
@output(m.BasicPropertyRead(many=True), example=ex.get_properties_response_example)
@doc(summary='Get a list of properties', description="Filters are optional. To make 'or more' queries add a '+' "
                                                     "symbol next to the number."
                                                     "Page number starts from 1 and per page displays the number of "
                                                     "properties indicated.")
def read_property(options):
    result = c.all_props(options)
    if result[0] == ControllerStatus.ERROR:
        abort(500)
    return result[1]


@router.put("/property")
@input(m.PropertyUpdate, examples=ex.put_property_request_examples)
@output({}, 204)
@doc(summary="Update a property's details", responses={
    404: "The property you're trying to edit doesn't exist on the database",
    403: "The property you're trying to edit doesn't belong to you"
})
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
@input(m.PropertyDelete, example=ex.delete_property_request_example)
@output({}, 204)
@doc(summary="Delete a property", responses={
    404: "The property you're trying to delete doesn't exist on the database",
    403: "The property you're trying to delete doesn't belong to you"
})
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


@router.get("/property")
@input(m.PropertyDataRequest, location="query", example=ex.get_property_request_example)
@output(m.PropertyDataResponse, example=ex.get_property_response_example)
@doc(summary="Get full details of a property", responses={
    404: "The property you're trying to look for doesn't exist in the database"
})
def get_property_data(data):
    result = c.get_property_data(data["id"])
    if result[0] == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    if result[0] == ControllerStatus.ERROR:
        abort(500)

    return result[1]


@router.post("/property/photos")
@input(m.UploadPhotosRequest)
@input(m.UploadPhotosQueryRequest, location="form")
@input(m.UploadPhotosFilesRequest, location="files")
@output({}, 204)
@doc(summary="Upload property's photos", responses={
    404: "The property you're trying to upload pictures doesn't exist on the database",
    403: "The property you're trying to upload pictures doesn't belong to you"
})
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


@router.get("/property/photo/<photo_id>")
@doc(hide=True)
def get_photo(photo_id):
    result = p.get_photo_from_db(photo_id)
    if result[0] == ControllerStatus.DOES_NOT_EXISTS:
        abort(404)

    return send_file(result[1], mimetype=f"image/{result[1].format.lower()}")
