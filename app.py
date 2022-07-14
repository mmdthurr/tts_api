import os
from flask import Flask, request
from pydantic import ValidationError
from flask_mongoengine import MongoEngine
from ariana import InternalError, error_wrapper, MakeAriana, Audio, User, Read, Search
from dotenv import load_dotenv
from mongoengine import Q

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv('DB'),

}
db = MongoEngine(app)


@app.route('/')
def root():
    return {'ok': 1}


@app.route('/tts/read/<string:token>', methods=['POST'])
def read_text(token):
    if request.data and token:
        if (user_obj := User.objects(token=token, active=True).first()) is None:
            return error_wrapper(401, [
                {'scope': ['token'], 'description': 'token not valid'}
            ])
        else:
            print(user_obj)
            try:
                r = Read(**request.json)
                try:
                    tts_obj = MakeAriana.easy_cache_tts(
                        byte_stream=MakeAriana.raw_ariana(
                            text=r.Text,
                            speaker=r.Speaker,
                            pitch_level=str(r.PitchLevel),
                            punctuation_level=str(r.PunctuationLevel),
                            speech_speed_level=str(r.SpeechSpeedLevel),
                            tone_level=str(r.ToneLevel),
                            gain_level=str(r.GainLevel),
                            beginning_silence=str(r.BeginningSilence),
                            ending_silence=str(r.EndingSilence),
                            format=r.Format,
                            quality=r.Quality,
                            api_key=user_obj.api_key
                        ),
                        mime=r.mime
                    )
                    Audio(
                        owner=token,
                        file_name=tts_obj.file_name,
                        mime=tts_obj.mime,
                        private=user_obj.make_new_private,
                        meta_data=request.json
                    ).save()
                    return {
                        'url': tts_obj.url,
                        'mime': tts_obj.mime,
                        'meta': request.json
                    }
                except InternalError as e:
                    return error_wrapper(
                        500,
                        [{'scope': [e.step], 'description': e.msg}]
                    )
            except ValidationError as e:
                return error_wrapper(
                    400,
                    [{'scope': list(er.get('loc')), 'description': er.get('msg')} for er in e.errors()]
                )


@app.route('/tts/search/<string:token>', methods=['POST'])
def search_audio(token):
    if request.data and token:
        if User.objects(token=token, active=True) is None:
            return error_wrapper(401, [
                {'scope': ['token'], 'description': 'token not valid'}
            ])
        else:
            try:
                search_obj = Search(
                    **request.json
                )
                search_dict = {'meta_data__Text__contains': search_obj.Text}
                if search_obj.Speaker:
                    search_dict['meta_data__Speaker'] = search_obj.Speaker
                if search_obj.Format:
                    search_dict['meta_data__Format'] = search_obj.Format
                if search_obj.Quality:
                    search_dict['meta_data__Quality'] = search_obj.Quality

                if (audio_obj := Audio.objects((Q(private=False) | Q(owner=token)), **search_dict)) is not None:
                    _to = search_obj.Page * 20
                    _from = _to - 20
                    return {
                        'audio': [{'url': f"{os.getenv('DL')}/tts/{a.file_name}.{a.mime}",
                                   'meta': a.meta_data} for a in audio_obj[_from:_to]]
                    }
                else:
                    return None
            except ValidationError as e:
                return error_wrapper(
                    400,
                    [{'scope': list(er.get('loc')), 'description': er.get('msg')} for er in e.errors()]
                )


if __name__ == '__main__':
    load_dotenv()
    app.run()
