import mongoengine as me


class Audio(me.Document):
    owner = me.StringField()
    file_name = me.StringField()
    mime = me.StringField()
    private = me.BooleanField()
    meta_data = me.DictField()


class User(me.Document):
    token = me.StringField()
    api_key = me.StringField()
    tg_uid = me.IntField()
    active = me.BooleanField()
    make_new_private = me.BooleanField()
