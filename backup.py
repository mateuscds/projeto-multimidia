##### IMPORTS #####

import moviepy.editor as mpy
from pydub import AudioSegment
import librosa
import numpy as np
from scipy.stats import uniform
import itertools
import time
import datetime

##### GLOBAL DEFINITIONS #####

vcodec =   "libx264"
videoquality = "24"
compression = "slow"
min_interval_between_beats = 2 #minimal time interval between beats (seconds)

##### PARAMETERS #####

input_music_path = 'music.mp3'
input_video_paths = ['example_data/example_1.mp4', 'example_data/example_2.mp4', 'example_data/example_3.mp4', 'example_data/example_4.mp4']
output_video_path = 'example_data/output.mp4'

##### FUNCTIONS #####

def read_mp3(music_path):
    
    """MP3 to numpy array"""
    
    a = AudioSegment.from_mp3(music_path)
    y = np.array(a.get_array_of_samples(), dtype = np.float32) / 2**15
    
    if a.channels == 2:
        y = y.reshape((-1, 2))
        y = y.mean(axis = 1)

    y = y[::2]
    sr = a.frame_rate//2
      
    return y, sr

def get_beat_times(music_path):
    
    """Detects beat times from music_path"""
    
    y, sr = read_mp3(music_path)

    onset_env = librosa.onset.onset_strength(y, sr = sr)
    prior = uniform(30, 300)
    utempo = librosa.beat.tempo(onset_envelope = onset_env, sr = sr, prior = prior)[0]

    _, beat_times = librosa.beat.beat_track(y = y, sr = sr, units = 'time', bpm = utempo)

    return beat_times

def standardize_beat_times(beat_times, min_interval_between_beats):
    
    """Shorttens the intervals between beats"""

    new_beat_times = []
    previous_beat = 0

    for beat in beat_times:
        if (beat - previous_beat) >= min_interval_between_beats:
            new_beat_times.append(beat) 
            previous_beat = beat

    return new_beat_times

def cut_and_mute_video(video_object, time_limits):

    """Cuts and muttes a video"""

    clip = video_object.subclip(time_limits[0], time_limits[1]) #cutting video
    muted_clip = clip.without_audio() #mutting video
    return muted_clip

def add_audio_to_video(video, music_path):

    """Adds audio to video clip"""
    music = mpy.AudioFileClip(music_path) 
    videoclip = video.set_audio(music)
    return videoclip

def calculate_interval_sizes(new_beat_times):

    """Calculate interval sizes of videos we need"""

    interval_sizes = []
    start_time = 0

    for beat in new_beat_times:
        interval = beat - start_time
        interval_sizes.append(interval)
        start_time = beat

    return interval_sizes

def get_video_scenes(interval_sizes):

    cursors = {}
    for video in input_video_paths:
        cursors[video] = 0

    video_scenes_list = []
    for interval, video_path in zip(interval_sizes, itertools.cycle(input_video_paths)):
        begining = str(datetime.timedelta(seconds = cursors[video_path]))
        end = str(datetime.timedelta(seconds = cursors[video_path] + interval))
        cursors[video_path] = cursors[video_path] + interval
        time_limits = [begining, end]
        video = mpy.VideoFileClip(video_path)
        video_scene = cut_and_mute_video(video, time_limits)
        video_scenes_list.append(video_scene)
    video.close()
    return video_scenes_list

if __name__ == '__main__':

    beat_times = get_beat_times(input_music_path)
    new_beat_times = standardize_beat_times(beat_times, min_interval_between_beats)
    interval_sizes = calculate_interval_sizes(new_beat_times)
    video_scenes_list = get_video_scenes(interval_sizes)
    final_video = mpy.concatenate_videoclips(video_scenes_list)
    final_clip = add_audio_to_video(final_video, input_music_path)
    final_clip.write_videofile(output_video_path, threads=4, fps=24,
                               codec=vcodec,
                               preset=compression,
                               ffmpeg_params=["-crf",videoquality])

