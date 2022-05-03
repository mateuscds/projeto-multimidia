##### IMPORTS #####

import moviepy.editor as mpy
from pydub import AudioSegment
import librosa
import numpy as np
from scipy.stats import uniform

##### GLOBAL DEFINITIONS #####

vcodec =   "libx264"
videoquality = "24"
compression = "slow"
min_interval_between_beats = 3 #minimal time interval between beats (seconds)

##### PARAMETERS #####

input_music_path = 'music.mp3'
input_video_paths = ['exemple_1.mp4', 'exemple_2.mp4', 'exemple_3.mp4']
output_video_path = 'output.mp4'

# modify these start and end times for your subclips
'''cuts = [('00:00:02.949', '00:00:20.152'),
        ('00:00:30.328', '00:00:40.077')]'''

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

def add_audio_to_video(video, audio):

    """Adds audio to video clip"""

    videoclip = video.set_audio(audio)
    return videoclip

'''
def convert_into_time_cuts(new_beat_times):

    # Formato tem que ser 
    # cuts = [('00:00:02.949', '00:00:20.152'), ('00:00:30.328', '00:00:40.077')]

    clip_cuts = []
    begin_beat = 0

    for beat in new_beat_times: # tem que ser em pares

            
        clip_cuts.append(cut)
        

    return clip_cuts

def edit_video(loadtitle, savetitle, cuts):
    
    # cut file
    clips = []
    for cut in cuts:

        # load file
        video = mpy.VideoFileClip(loadtitle)

        clip = cut_and_mute_video(video, cut)
        clips.append(clip)


    final_clip = mpy.concatenate_videoclips(clips)


    # putting music into cutted video

    music = mpy.AudioFileClip("music.mp3") 
    final_clip = add_audio_to_video(final_clip, music)

    # save file
    final_clip.write_videofile(savetitle, threads=4, fps=24,
                               codec=vcodec,
                               preset=compression,
                               ffmpeg_params=["-crf",videoquality])

    video.close()
'''

if __name__ == '__main__':

    beat_times = get_beat_times(input_music_path)
    new_beat_times = standardize_beat_times(beat_times, min_interval_between_beats)

    print(new_beat_times)

    #a partir dos beat times, deveremos descobrir os intervalos entre cada um dos beats, para saber o comprimento de pedaços de vídeos que precisamos

    #com esses intervalos em mão, para cada vídeo de entrada iremos definir limites de tempo que representem uma parte do vídeo com um dos comprimentos (podemos seguir a ordem -> primeiro vídeo = primeiro intervalo)
    #esse pedaço pode começar do ínicio, meio, aleatório ou fim do vídeo

    #depois que tivermos esses limites, iremos realizar o corte de cada vídeo

    #depois com todos os vídeos cortados, iremos juntar todos

    #por fim, adicionaremos a música e salvaremos

    #clip_cuts = convert_into_time_cuts(new_beat_times)

    #edit_video(loadtitle, savetitle, cuts)