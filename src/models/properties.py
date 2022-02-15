from mongoengine import Document, StringField, DecimalField, IntField, ListField


# general properties info fields
class PropertyData(Document):
    address = StringField()
    description = StringField()
    price = DecimalField()
    terrain_height = DecimalField()
    terrain_width = DecimalField()
    bed = IntField()
    bath = DecimalField()
    floors = IntField()
    garage = IntField()
    photo_list = ListField()
    contract = StringField()
    currency = StringField()
    meta = {"collection": "properties"}
