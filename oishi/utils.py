import subprocess
import os


def convert_mp3_2_wav(input_path, output_path, sampling_rate='16k'):
    subprocess.call(['sox', input_path, output_path, 'channels', '1'])


def convert_all_mp3_to_wav(mp3_folder, wav_folder, sampling_rate='16k'):
    for f in os.listdir(mp3_folder):
        input_path = mp3_folder + "/" + f
        output_path = wav_folder + "/" + f.replace("mp3", "wav")
        convert_mp3_2_wav(input_path, output_path)


if __name__ == "__main__":
    mp3_folder = 'recordings/mp3'
    wav_folder = 'recordings/wav'
    convert_all_mp3_to_wav(mp3_folder, wav_folder)
