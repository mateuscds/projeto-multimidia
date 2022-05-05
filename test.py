from editor import Editor

input_music_path = 'example_data/music2.mp3'
input_video_paths = ['example_data/example_1.mp4', 'example_data/example_2.mp4', 'example_data/example_3.mp4', 'example_data/example_4.mp4']
output_video_path = 'example_data/output2.mp4'

min_interval_between_beats = 2

editor = Editor(input_music_path, input_video_paths, output_video_path, min_interval_between_beats)
editor.merge()