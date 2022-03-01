get_properties_response_example = [
    {"address": "1600 Penn Street", "bath": 2.5, "bed": 7, "contract": "sell", "currency": "USD", "floors": 2,
     "garage": 3, "owner_username": "potus", "price": 30157628240789, "property_id": "605cdc42f3ac32a19e4deb80",
     "terrain_height": 65, "terrain_width": 70, "thumbnail_id": "605cdd42f3ac32a19e4deb82"},
    {"address": "1273 Rockefeller Street", "bath": 1.5, "bed": 3, "contract": "rent", "currency": "EUR", "floors": 2,
     "garage": 2, "owner_username": "xX_bacon_hair_Xx", "price": 1580000, "property_id": "60772237a651cad33ea0510f",
     "terrain_height": 7, "terrain_width": 9.5, "thumbnail_id": "60770f747aa829e4fc9ed8e5"}]
delete_property_request_example = {"id": "6077a5d0a651cad33ea05115"}
get_property_request_example = {"id": "60779d597aa829e4fc9ed8ec"}
get_property_response_example = {"address": "3RFG+MFG, Pyongyang, North Korea", "bath": 1, "bed": 1, "contract": "sell",
                                 "currency": "KPW", "description": "평양 직할시 평양", "floors": 1, "garage": 50,
                                 "owner_info": {"username": "kjun"},
                                 "photo_ids": ["60779d597aa829e4fc9ed8ec", "60770f747aa829e4fc9ed8e5",
                                               "605cdc42f3ac32a19e4deb80"], "price": 15752369.22, "terrain_height": 40,
                                 "terrain_width": 50}
post_property_request_example = {"address": "1273 Rockefeller Street", "bath": 1.5, "bed": 3, "contract": "rent",
                                 "currency": "EUR", "floors": 2, "garage": 2, "price": 1580000, "terrain_height": 7,
                                 "terrain_width": 9.5}
post_property_response_example = {"id": "60772237a651cad33ea0510f"}
put_property_request_examples = {
    "second": {"summary": "Change property dimensions and price",
               "value": {"id": "60772237a651cad33ea0510f", "terrain_height": 11,
                         "terrain_width": 7.5, "price": 850000}},
    "first": {"summary": "Change property description",
              "value": {"id": "60772237a651cad33ea0510f",
                        "description": "New property description"}}}
