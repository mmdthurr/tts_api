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
    ariana_setting = me.DictField(default={

        'Speaker': 'Male2',
        'PitchLevel': 4,
        'PunctuationLevel': 2,
        'SpeechSpeedLevel': 5,
        'ToneLevel': 10,
        'GainLevel': 3,
        'BeginningSilence': 0,
        'EndingSilence': 0,

    })
    # ariana_setting:dict =                         speaker=r.Speaker,
    #     #     #                     pitch_level=str(r.PitchLevel),
    #     #     #                     punctuation_level=str(r.PunctuationLevel),
    #     #     #                     speech_speed_level=str(r.SpeechSpeedLevel),
    #     #     #                     tone_level=str(r.ToneLevel),
    #     #     #                     gain_level=str(r.GainLevel),
    #     #     #                     beginning_silence=str(r.BeginningSilence),
    #     #     #                     ending_silence=str(r.EndingSilence),
