##### IMPORTS #####

import moviepy.editor as mpy
from pydub import AudioSegment
import librosa
import numpy as np
from scipy.stats import uniform
import itertools
import datetime
import soundfile as sf
import random

from utils import remove_temp_files


class SynchroEditor:
    vcodec =   "libx264"
    videoquality = "24"
    compression = "slow"
    min_interval_between_moments = 2

    input_music_path = 'example_data/music.mp3'
    input_video_paths = ['example_data/example_1.mp4', 'example_data/example_2.mp4', 'example_data/example_3.mp4', 'example_data/example_4.mp4']
    output_video_path = 'example_data/output.mp4'

    music_wave =  None
    music_sr = None
    clicks = None
    clicks_moments = []

    originall_moments = None
    moments = None

    final_video = None

    def __init__(self, input_music_path=None, input_video_paths=None, output_video_path=None):
        if input_music_path!=None:
            self.input_music_path = input_music_path
        if input_video_paths!=None:
            self.input_video_paths = input_video_paths
            random.shuffle(self.input_video_paths)
        if output_video_path!=None:
            self.output_video_path = output_video_path
        
    
    def set_vcodec(self, vcodec):
        """Sets video codec"""
        self.vcodec = vcodec
    
    def set_videoquality(self, videoquality):
        """Sets video quality"""
        self.videoquality = videoquality
    
    def set_compression(self, compression):
        """Sets compression"""
        self.compression = compression
    
    def set_min_interval_between_moments(self, min_interval_between_moments):
        """Sets minimal time interval between beats"""
        self.min_interval_between_moments = min_interval_between_moments

    def read_mp3(self, music_path):
        """MP3 to numpy array"""
        
        a = AudioSegment.from_mp3(music_path)
        y = np.array(a.get_array_of_samples(), dtype = np.float32) / 2**15

        self.music_length = a.duration_seconds
        
        if a.channels == 2:
            y = y.reshape((-1, 2))
            y = y.mean(axis = 1)

        y = y[::2]
        sr = a.frame_rate//2

        self.music_sr = sr
        self.music_wave = y
        

    def get_moments(self):
        """Detects beat times from music_path"""
        
        self.read_mp3(self.input_music_path)

        onset_env = librosa.onset.onset_strength(self.music_wave, sr = self.music_sr)
        prior = uniform(30, 300)
        utempo = librosa.beat.tempo(onset_envelope = onset_env, sr = self.music_sr, prior = prior)[0]

        if self.method=='beat':
            _, moments = librosa.beat.beat_track(y = self.music_wave, sr = self.music_sr, units = 'time', bpm = utempo)
        elif self.method=='onset':
            moments = librosa.onset.onset_detect(y = self.music_wave, sr = self.music_sr, units = 'time')

        return moments

    def standardize_moments(self):
        """Shorttens the intervals between beats"""

        new_moments = []
        previous_beat = 0

        for beat in self.moments:
            if (beat - previous_beat) >= self.min_interval_between_moments:
                new_moments.append(beat) 
                previous_beat = beat

        self.clicks_moments = librosa.clicks(new_moments, sr=self.music_sr, length=len(self.music_wave))
        self.originall_moments = self.moments
        self.moments = new_moments


    def cut_and_mute_video(self, video_object, time_limits):
        """Cuts and muttes a video"""

        clip = video_object.subclip(time_limits[0], time_limits[1]) #cutting video
        muted_clip = clip.without_audio() #mutting video
        return muted_clip

    def add_audio_to_video(self):
        """Adds audio to video clip"""
        if self.clicks:    
            sf.write(self.input_music_path.replace('.mp3','_clicks.wav'), self.music_wave+self.clicks_moments, self.music_sr)
            music = mpy.AudioFileClip(self.input_music_path.replace('.mp3','_clicks.wav'))
        else:
            music = mpy.AudioFileClip(self.input_music_path)
        videoclip = self.final_video.set_audio(music)
        return videoclip

    def calculate_interval_sizes(self):
        """Calculate interval sizes of videos we need"""

        interval_sizes = []
        start_time = 0

        for beat in self.moments:
            interval = beat - start_time
            interval_sizes.append(interval)
            start_time = beat
        
        interval_sizes.append(self.music_length - start_time)

        return interval_sizes

    def get_video_scenes(self, interval_sizes):
        """Gets video scenes"""

        cursors = {}
        for video in self.input_video_paths:
            cursors[video] = 0

        video_scenes_list = []
        for interval, video_path in zip(interval_sizes, itertools.cycle(self.input_video_paths)):
            begining = str(datetime.timedelta(seconds = cursors[video_path]))
            end = str(datetime.timedelta(seconds = cursors[video_path] + interval))
            cursors[video_path] = cursors[video_path] + interval
            time_limits = [begining, end]
            video = mpy.VideoFileClip(video_path)
            video_scene = self.cut_and_mute_video(video, time_limits)
            video_scenes_list.append(video_scene)
        return video_scenes_list
    
    def concatenate_videos(self, video_scenes_list):
        """Concatenates videos"""
        video = mpy.concatenate_videoclips(video_scenes_list)
        self.final_video = video
        return video

    def write_video(self, threads=4, fps=24):
        """Writes video"""

        
        self.final_video.write_videofile(self.output_video_path,
                                         threads=threads,
                                         fps=fps,
                                         codec=self.vcodec,
                                         preset=self.compression,
                                         ffmpeg_params=["-crf",self.videoquality])
        
        remove_temp_files()

    def merge(self, method='beat', clicks=False, min_interval_between_moments=2):
        """Runs the whole process"""
        self.method = method
        self.clicks = clicks
        self.min_interval_between_moments = min_interval_between_moments
        
        print('Reading music and get beat times...')
        self.moments = self.get_moments()
        print('Standardizing beat times...')
        self.standardize_moments()
        print('Calculating interval beats...')
        interval_sizes = self.calculate_interval_sizes()
        print('Getting video scenes...')
        video_scenes_list = self.get_video_scenes(interval_sizes)
        print('Concatenating videos...')
        self.final_video = self.concatenate_videos(video_scenes_list)
        print('Adding audio to video...')
        self.final_video = self.add_audio_to_video()
        print('Writing video...')
        self.write_video()
        return self.output_video_path
