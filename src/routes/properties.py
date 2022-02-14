from apiflask import APIBlueprint, input, output, abort, doc
from apiflask.schemas import Schema

from ..controllers.properties import all_props, delete_prop, register_prop, update_prop
from ..models.properties import PropertyData
from ..utils.enums import ControllerStatus

router = APIBlueprint("prop", __name__, "Properties", url_prefix="/api/properties")

@router.get('/')
def test():
    return {'message': 'OK'}

#register
@router.post("/register-property")
@input(PropertyData)
@output(Schema, 201)
@doc(summary='Creates properties')
def create_property(data):
    result = register_prop(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    
    return ""

#read
@router.get("/properties")
@output(Schema, 200)
@doc(summary='Get properties info')
def read_property(data):
    result = all_props(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    return ""


#update
@router.put("/property-{id}")#not sure about id xD
@input(PropertyData)#not sure if using just id's from property
@output(Schema, 200)
@doc(summary="Update properties based on their ID")
def update_property(data):
    result = update_prop(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    return ""



#delete
@router.delete("/property-{id}")#not sure about id xD
@input(PropertyData)#not sure if using just id's from property x2
@output(Schema, 202)
@doc(summary="Delete properties based on their ID")
def delete_property(data):
    result = delete_prop(data)
    if result == ControllerStatus.ERROR:
        abort(500)
    return ""