import mongoengine as me


class Token(me.Document):
    meta = {"collection": "tokens"}
    owner = me.ReferenceField("User", dbref=True, required=True, unique=True)
    access_token = me.StringField()
    refresh_token = me.StringField()
    access_token_expires = me.DateTimeField(required=True)
    refresh_token_expires = me.DateTimeField(required=True)
