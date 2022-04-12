import moviepy.editor as mpy

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


if __name__ == '__main__':
    edit_video(loadtitle, savetitle, cuts)