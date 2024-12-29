import os


current_directory = os.getcwd().__str__()
os.chdir(current_directory+'/wav2lip/Wav2Lip')

folder_path = "/home/lukasz/programminglearningnowy/programming_learning/labdl/pythonProject/MarxStirner/"
photo1_folder_path = folder_path+"Marx.jpg"
photo2_folder_path = folder_path+"Stirner.jpg"

output_file_path = folder_path + "output.mp4"
program_path = current_directory+"/wav2lip/Wav2Lip/inference.py"
checkpoints_path = current_directory+"/wav2lip/Wav2Lip/checkpoints/wav2lip_gan.pth"


import subprocess
files = sorted(os.listdir(folder_path))
print(files)
for file_name in files:
    print(file_name[-4:])
    if file_name[-4:] == '.mp3':
        audio_path = os.path.join(folder_path, file_name).__str__()
        if file_name[0] == 'a':
            photo_path = folder_path+"Marx.jpg"
            output_file_path = audio_path[:-4] + ".mp4"
            command = "python " + program_path + " --checkpoint_path " + checkpoints_path + " --face " + photo_path + " --audio " + audio_path + " --outfile " + output_file_path
            print(command)
            subprocess.run(command, shell=True)
        elif file_name[0] == 't':
            photo_path = folder_path + "Stirner.jpg"
            output_file_path = audio_path[:-4] + ".mp4"
            command = "python " + program_path + " --checkpoint_path " + checkpoints_path + " --face " + photo_path + " --audio " + audio_path + " --outfile " + output_file_path
            print(command)
            subprocess.run(command, shell=True)






