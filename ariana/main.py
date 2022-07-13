import datetime, uuid, ftplib, os, requests
from .error import InternalError
import io
from .models import User


class MakeAriana:

    def __init__(
            self,
            url,
            file_name,
            mime,
    ):
        self.url = url
        self.file_name = file_name
        self.mime = mime

    @staticmethod
    def raw_ariana(
            text,
            speaker,
            pitch_level,
            punctuation_level,
            speech_speed_level,
            tone_level,
            gain_level,
            beginning_silence,
            ending_silence,
            format,
            quality,
            api_key=os.getenv('KEY')
    ):
        res = requests.post(
            url='http://api.farsireader.com/ArianaCloudService/ReadText',
            json={
                'Text': text,
                'Speaker': speaker,
                'PitchLevel': pitch_level,
                'PunctuationLevel': punctuation_level,
                'SpeechSpeedLevel': speech_speed_level,
                'ToneLevel': tone_level,
                'GainLevel': gain_level,
                'BeginningSilence': beginning_silence,
                'EndingSilence': ending_silence,
                'Format': format,
                'Base64Encode': '0',
                'Quality': quality,
                'APIKey': api_key
            },
            timeout=50
        )
        if res.status_code in range(400, 600):
            User.objects(api_key=api_key).update(set__active=False)
            raise InternalError(step='req for byte stream', msg='some thing bad happened try later')
        else:
            return res.content

    @classmethod
    def easy_cache_tts(cls, byte_stream, mime):
        file_name = f'{str(uuid.uuid4())[-12:]}_{int(datetime.datetime.utcnow().timestamp())}'
        try:
            with ftplib.FTP(host=os.getenv('FTP'), user=os.getenv('FTP_USER'),
                            passwd=os.getenv('FTP_PASS')) as ftp_session:
                with io.BytesIO(byte_stream) as f:
                    ftp_session.storbinary(f'STOR public_html/tts/{file_name}.{mime}', f)
            return cls(
                url=f"{os.getenv('DL')}/tts/{file_name}.{mime}",
                file_name=file_name,
                mime=mime
            )
        except ftplib.all_errors:
            raise InternalError(step='FTP', msg='ftp server not accessible')
