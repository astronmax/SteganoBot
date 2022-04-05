from os import path
from pydub import AudioSegment


def convert_mp3_to_wav(source, output):
    sound = AudioSegment.from_mp3(source)
    sound.export(output, format="wav")
