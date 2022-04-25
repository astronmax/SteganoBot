from os import path
from pydub import AudioSegment


def convert_mp3_to_wav(source, output):
    """
    Converts .mp3 file to .wav file

    :param source: .mp3 file name
    :type source: str
    :param output: .wav file name
    :type output: str
    :return: None
    """
    sound = AudioSegment.from_mp3(source)
    sound.export(output, format="wav")
