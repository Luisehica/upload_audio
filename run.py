from __future__ import unicode_literals

import ffmpeg as ffmpeg
from pytube import YouTube
import ssl
import os
import subprocess
import pandas as pd

DESTINATION = './results/'


class Person:
    """
    Entity to a person voice data.
    """
    def __init__(self, name):
        self.name = name
        self.dir = os.path.join(DESTINATION, name)
        self.resources = []

    def add_resource(self, resource):
        self.resources.append(resource)


class Resources:
    """
    """
    filename = ''
    def __init__(self, url, list_chunk_times):
        self.url = url
        self.list_chunk_times = list_chunk_times

    def filename(self, person_name, resource_name, duration):
        self.filename = f"{person_name}-{resource_name}-{duration}.wav"

    def download_yt(self, dir):
        yt = YouTube(self.url)
        
        video = yt.streams.filter(only_audio=True).first()

        video.download(dir)
        
        default_filename = video.default_filename

        duration = get_length(os.path.join(dir, default_filename))
        filename(self, person_name, resource_name, duration)

        # using pytube API
        stream = ffmpeg.input(os.path.join(dir, default_filename))
        stream = ffmpeg.output(stream,
                                os.path.join(dir, self.filename))
        ffmpeg.run(stream)
        os.remove(os.path.join(dir, default_filename))
        

    def trim_audio(self, start, end):
        pass
    



def get_length(input_audio):
    """
    Calculate duration audio in seconds
    :param input_audio: The paht of audio
    :return:
    """
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_audio], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)


if __name__ == '__main__':

    df = pd.read_csv("Audios.csv")

    print(df)
    os.exit

    # Create destination directory
    if not os.path.exists(DESTINATION):
        os.mkdir(DESTINATION)

    persons = [Person('LUIS FERNANDO VELASCO')]
    print(voices[0].dir)
    os.exit_()
    try:
        ssl._create_default_https_context = ssl._create_unverified_context

        for person in persons:

            dir = os.path.join(DESTINATION, voice.name) 

            res = Resources(url, list_chunk_times)

            # trim audio
            audio_input = ffmpeg.input(os.path.join(dir, new_filename))
            #audio_cut = audio_input.audio.filter('atrim', duration=5)
            audio_cut = audio_input.audio.filter('atrim', start=30, end=40)
            audio_output = ffmpeg.output(audio_cut, os.path.join(dir, 'out.wav'))
            ffmpeg.run(audio_output)

    except Exception as ex:
        print("Not could download audio file")
        print(ex)
