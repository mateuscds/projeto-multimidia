import click
from editor import Editor
from utils import remove_temp_files

input_music_path = 'input/music/music2.mp3'
input_video_paths = ['input/videos/example_1.mp4',
                     'input/videos/example_2.mp4',
                     'input/videos/example_3.mp4',
                     'input/videos/example_4.mp4']
output_video_path = 'output/output5.mp4'

min_interval_between_moments = 0.75
method = 'onset'
clicks = True

editor = Editor(input_music_path, input_video_paths, output_video_path)
editor.merge(method, clicks, min_interval_between_moments)
