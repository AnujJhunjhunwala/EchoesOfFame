
from moviepy import VideoFileClip, concatenate_videoclips
import os

# Folder z plikami wideo
folder_path = "/home/lukasz/programminglearningnowy/programming_learning/labdl/pythonProject/MarxStirner/"

# Pobierz listę plików w folderze i posortuj alfabetycznie
video_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mkv'))])

videos_person1 = []
videos_person2 = []
for i in video_files:
    if i[0] == 'a':
        videos_person1.append(i)
    elif i[0] == 't':
        videos_person2.append(i)
# Utwórz listę obiektów VideoFileClip
video_clips = []
for i in range(videos_person1.__len__()):
    video_clips.append(VideoFileClip(os.path.join(folder_path, videos_person1[i])))
    if i < videos_person2.__len__():
        video_clips.append(VideoFileClip(os.path.join(folder_path, videos_person2[i])))

# Połącz wszystkie klipy
final_clip = concatenate_videoclips(video_clips, method="compose")

# Zapisz wynikowy plik wideo
output_path = folder_path+"merged_video.mp4"
final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

print("Wideo zostało połączone i zapisane jako:", output_path)
