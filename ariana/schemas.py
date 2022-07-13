from pydantic import BaseModel, validator


class Read(BaseModel):
    Text: str
    Speaker: str
    PitchLevel: int
    PunctuationLevel: int
    SpeechSpeedLevel: int
    ToneLevel: int
    GainLevel: int
    BeginningSilence: int
    EndingSilence: int
    Format: str
    Quality: str

    @validator('Speaker')
    def check_speaker(cls, v):
        if v not in ['Male1', 'Male2', 'Female1']:
            raise ValueError("must be in range ['Male1', 'Male2', 'Female1']")
        return v

    @validator('PitchLevel')
    def check_pitch(cls, v):
        if v not in range(1, 11):
            raise ValueError('must be in range 1-10')
        return v

    @validator('PunctuationLevel')
    def check_punctuation(cls, v):
        if v not in range(1, 4):
            raise ValueError('must be in range 1-3')
        return v

    @validator('SpeechSpeedLevel')
    def check_speech_speed(cls, v):
        if v not in range(1, 11):
            raise ValueError('must be in range 1-10')
        return v

    @validator('ToneLevel')
    def check_tone(cls, v):
        if v not in range(1, 20):
            raise ValueError('must be in range 1-19')
        return v

    @validator('GainLevel')
    def check_gain(cls, v):
        if v not in range(1, 6):
            raise ValueError('must be in range 1-5')
        return v

    @validator('BeginningSilence')
    def check_beginning_silence(cls, v):
        if v not in range(0, 6):
            raise ValueError('must be in range 0-5')
        return v

    @validator('EndingSilence')
    def check_ending_silence(cls, v):
        if v not in range(0, 6):
            raise ValueError('must be in range 0-5')
        return v

    @validator('Format')
    def check_format(cls, v):
        if v not in [
            'wav16',
            'alaw16',
            'mlaw16',
            'wav8',
            'alaw8',
            'mlaw8',
            'mp3',
            'ogg',
            'raw16'
        ]:
            raise ValueError("must be in range ['wav16','alaw16','mlaw16','wav8','alaw8','mlaw8','mp3','ogg','raw16']")
        return v

    @validator('Quality')
    def check_quality(cls, v):
        if v not in ['normal', 'low']:
            raise ValueError("must be in range ['normal', 'low']")
        return v

    @property
    def mime(self):
        if self.Format in [
            'wav16',
            'alaw16',
            'mlaw16',
            'wav8',
            'alaw8',
            'mlaw8',
            'raw16'
        ]:
            return 'wav'
        elif self.Format == 'mp3':
            return 'mp3'
        elif self.Format == 'ogg':
            return 'ogg'


class Search(BaseModel):
    Text: str
    Page: int
    Speaker: str = None
    Format: str = None
    Quality: str = None

    @validator('Page')
    def validate_p(cls, v):
        if v in range(1, 100):
            return v
        raise ValueError('must be in range 1-100')

    @validator('Speaker')
    def check_speaker(cls, v):
        if v not in ['Male1', 'Male2', 'Female1']:
            raise ValueError("must be in range ['Male1', 'Male2', 'Female1']")
        return v

    @validator('Format')
    def check_format(cls, v):
        if v not in [
            'wav16',
            'alaw16',
            'mlaw16',
            'wav8',
            'alaw8',
            'mlaw8',
            'mp3',
            'ogg',
            'raw16'
        ]:
            raise ValueError("must be in range ['wav16','alaw16','mlaw16','wav8','alaw8','mlaw8','mp3','ogg','raw16']")
        return v

    @validator('Quality')
    def check_quality(cls, v):
        if v not in ['normal', 'low']:
            raise ValueError("must be in range ['normal', 'low']")
        return v

# json = {
#     'Text': 'متن تست',
#     'Speaker': 'Male1',
#     'PitchLevel': 1,
#     'PunctuationLevel': 3,
#     'SpeechSpeedLevel': 5,
#     'ToneLevel': 2,
#     'GainLevel': 1,
#     'BeginningSilence': 0,
#     'EndingSilence': 0,
#     'Format': 'mp3',
#     'Quality': 'normal'
#
# }
# try:
#
#     print(Ariana(**json).__dict__)
# except ValidationError as e:
#     print([{'scope': list(error.get('loc')), 'description': error.get('msg')} for error in e.errors()])
