import datetime

import mongoengine as me


# logs ของ แต่ละ request
class RequestLog(me.EmbeddedDocument):
    user = me.ReferenceField("User", dbref=True)
    ip_address = me.StringField()  # ip address
    user_agent = me.StringField()  # user agent ที่ผู่ใช้ใช้งานเข้ามาของ browser
    action = me.StringField()  # ทำอะไร
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
