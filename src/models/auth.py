from mongoengine import Document, StringField, EmailField, BooleanField


class User(Document):
    username = StringField()
    email = EmailField()
    passwdHash = StringField()
    isVerified = BooleanField()
    lastToken = StringField()
    phone = StringField()
    contactEmail = StringField()
    fbLink = StringField()
    instaLink = StringField()
    twitLink = StringField()
