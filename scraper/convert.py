import os
import subprocess

path_file_ffmpeg = "C:\\project\\green-team\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"
path_dir_user = "C:\\Users\\JaapOosterbroek\\Desktop\\superpatient\\katiekickscancer"
path_dir_video = os.path.join(path_dir_user, "video")
path_dir_wav = os.path.join(path_dir_user, "wav")
if not os.path.isdir(path_dir_wav):
    os.makedirs(path_dir_wav)
    
for name_file in os.listdir(path_dir_video):
    id_post = name_file[:-4]
    print(id_post)
    path_file_source = os.path.join(path_dir_video, name_file)
    path_file_target = os.path.join(path_dir_wav, id_post + ".wav")
    if not os.path.isfile(path_file_target):
        print("is_doing")
        command = path_file_ffmpeg
        command += f" -i {path_file_source}"
        command += f"  -ac 2 -f wav {path_file_target}"
        print(command)
        subprocess.call(command)

#ffmpeg -i 7118872948852706606.mp4 -ac 2 -f wav 7118872948852706606.wav