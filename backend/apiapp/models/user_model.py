import datetime
import mongoengine as me
import bcrypt


class User(me.Document):
    meta = {
        "collection": "users",
        "indexes": [
            "username",
            "$username",
            "#username",
        ],
    }
    email = me.StringField(required=True, max_length=200, default="")
    username = me.StringField(required=True, max_length=200, unique=True)
    password = me.StringField(required=True, default="")
    title_name = me.StringField(required=True)
    first_name = me.StringField(required=True, max_length=200)
    last_name = me.StringField(required=True, max_length=200)
    status = me.StringField(required=True, default="active", max_length=15)
    roles = me.ListField(me.StringField(), default=["user"])
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    last_login_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )

    def has_roles(self, roles):
        for role in roles:
            if role in self.roles:
                return True
        return False

    def set_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(
            plain_password.encode("utf-8"), bcrypt.gensalt(14)
        ).decode()

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.password.encode("utf-8")
        )
