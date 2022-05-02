import moviepy.editor as mpy

from pydub import AudioSegment # to read mp3s 
import librosa # audio analysis 

from sys import argv
import numpy as np
from time import sleep, time

from scipy.stats import lognorm, uniform

vcodec =   "libx264"
videoquality = "24"

# slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "slow"

# PARAMETROS

title = "NEUROLAKE"
loadtitle = title + '.mp4'
savetitle = title + '_EDITADO' + '.mp4'

# modify these start and end times for your subclips
cuts = [('00:00:02.949', '00:00:20.152'),
        ('00:00:30.328', '00:00:40.077')]

# Mínimo de tempo entre as batidas

min_time_beat = 3 #segundos

########################### FUNÇÕES DE TRATAMENTO DAS BATIDAS ###########################


def read_mp3(filename):
    """MP3 to numpy array"""
    a = AudioSegment.from_mp3(filename)
    y = np.array(a.get_array_of_samples(), dtype=np.float32) / 2**15
    
    if a.channels == 2:
        y = y.reshape((-1, 2))
        y = y.mean(axis=1) # stripping to mono

    # reducing sample rate (div by 2)
    y = y[::2]
    sr = a.frame_rate//2
      
    return y, sr

   
def read_wav(filename):
    """WAV to numpy array"""
    y, sr = librosa.load(filename)
    return y, sr

def read_any(filename):
    """WAV or MP3 to numpy array"""
    if filename.endswith('.mp3'):
        return read_mp3(filename)
    elif filename.endswith('.wav'):
        return read_wav(filename)
    else:
        print("Unknown file extension")
        # exception or sth
        return 
    
def mp3_to_wav(src, dst=None):
    """Exports mp3 file to wav"""
    dst = dst or src.replace('.mp3', '.wav')
    audio = AudioSegment.from_mp3(src)
    audio.export(dst, format="wav")


def get_beat_times(filename=None, y=None, sr=None):
    """Detects beat times from filename or np.arrray"""
    if filename is not None:
        y, sr = read_any(filename)
    if y is not None and sr is not None:
        pass # y, sr already loaded
    else:
        print("Something wrong with the arguments")
        return

    onset_env = librosa.onset.onset_strength(y, sr=sr)
    prior = uniform(30, 300)  # uniform over 30-300 BPM
    utempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, prior=prior)[0]

    _, beat_times = librosa.beat.beat_track(y=y, sr=sr, units='time', bpm=utempo)

    return beat_times, utempo


########################### FUNÇÕES DE TRATAMENTO DOS VIDEOS ###########################


def cut_and_mute_video(video, limits):

    # cut file
    clip = video.subclip(limits[0], limits[1])

    muted_clip = clip.without_audio()

    return muted_clip


def audio_into_clip(video, audio):

    # adding audio to the video clip
    videoclip = video.set_audio(audio)
    return videoclip


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
    final_clip = audio_into_clip(final_clip, music)

    # save file
    final_clip.write_videofile(savetitle, threads=4, fps=24,
                               codec=vcodec,
                               preset=compression,
                               ffmpeg_params=["-crf",videoquality])

    video.close()


def standard_beat_times(beat_times, min_time_beat):

    new_beat_times = []
    previous_beat = 0

    for beat in beat_times:

        if beat - previous_beat >= min_time_beat:
            new_beat_times.append(beat) 
            previous_beat = beat


    return new_beat_times


def convert_into_time_cuts(new_beat_times):

    # Formato tem que ser 
    # cuts = [('00:00:02.949', '00:00:20.152'), ('00:00:30.328', '00:00:40.077')]

    clip_cuts = []
    begin_beat = 0

    for beat in new_beat_times: # tem que ser em pares

            
        clip_cuts.append(cut)
        

    return clip_cuts


if __name__ == '__main__':

    beat_times, _ = get_beat_times('music.mp3')
    new_beat_times = standard_beat_times(beat_times, min_time_beat) #lista atualizada com o minimo de tempo que a batida tem que ter

    print(new_beat_times)

    # Agora, temos que converter para o formato de cuts

    clip_cuts = convert_into_time_cuts(new_beat_times)

    edit_video(loadtitle, savetitle, cuts)