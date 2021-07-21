from __future__ import unicode_literals

import ffmpeg as ffmpeg
from pytube import YouTube
import ssl
import os
import subprocess

import pandas as pd
import numpy as np

DESTINATION = './results/'


class Person:
    """
    Entity to a person voice data.
    """
    def __init__(self, name, df):
        self.name = name
        self.dir = os.path.join(DESTINATION, name)
        self.df = df
        
        
    @property
    def filtered_df(self):
        df = self.df
        mask = df['Nombre']==self.name
        filtered_df = df[mask]
        return filtered_df

    @property
    def resources(self):
        return self.filtered_df['URL']

    @property
    def trims(self):
        filtered_df = self.filtered_df
        columns_trim = list(filtered_df.columns[3:])
        filtered_df['trims'] = filtered_df[columns_trim].apply(lambda x: [i for i in x], axis=1)
        return filtered_df[['URL', 'trims']]


class Resources:
    """
    """
    def __init__(self, Person):
        self.person_name = Person.name
        self.list_url = Person.resources                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        self.list_trims = Person.trims
        self.dir_folder = Person.dir

    def create_filename(self, resource_name, duration):
        """[summary]

        Args:
            resource_name ([type]): [description]
            duration ([type]): [description]

        Returns:
            [type]: [description]
        """
        return f"{self.person_name}-{resource_name}-{duration}.wav"

    def get_duration(self, input_audio):
        """Calculate duration audio in seconds

        Args:
            input_audio ([type]): Path of audiofile

        Returns:
            float: duration of audio in seconds
        """

        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_audio], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)

    def download_yt(self, url):
        """Download yt video using pytube

        Args:
            url ([type]): [description]
        """
        yt = YouTube(url)
        
        video = yt.streams.filter(only_audio=True).first()

        video.download(self.dir_folder)
        
        default_filename = video.default_filename

        duration = self.get_duration(os.path.join(dir, default_filename))
        new_dir_filename = self.create_filename(default_filename[:7], duration)

        stream = ffmpeg.input(os.path.join(dir, default_filename))
        stream = ffmpeg.output(stream,
                                os.path.join(dir, new_dir_filename))
        ffmpeg.run(stream)
        os.remove(os.path.join(dir, default_filename))
        return new_dir_filename
        
    def trim_audio(self, new_dir_filename):
        trims = self.list_trims
        new_trims = []
        # TODO: revisar que si quede una lista de listas con las parejas de cada recorte
        for i in range(len(trims)/2):
            new_trims.append([trims[i*2], trims[i*2+1]])

        for trim in new_trims:

            audio_input = ffmpeg.input(new_dir_filename)
            audio_cut = audio_input.audio.filter('atrim', start=trim[0], end=trim[1])
            
        audio_output = ffmpeg.output(audio_cut, os.path.join(self.dir_folder, 'out.wav'))
        ffmpeg.run(audio_output)

    

if __name__ == '__main__':

    # Create destination directory
    if not os.path.exists(DESTINATION):
        os.mkdir(DESTINATION)

    df = pd.read_csv("Audios.csv")
    names_congr = df['Nombre'].unique()

    for congr in names_congr:
        congressman = Person(congr, df)
        resources = Resources(congressman)
        
        try:
            ssl._create_default_https_context = ssl._create_unverified_context

            for url in resources.list_url:
                new_dir_filename = Resources.download_yt(url)
                Resources.trim_audio(new_dir_filename)

        except Exception as ex:
            print("Not could download audio file")
            print(ex)