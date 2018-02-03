from os import listdir
from os.path import isfile, join


folder_path = 'oishi/oh/cnsc/libs/'

# Receives an array of


def run_cnsc(transcript, filename):
    meta_file = filename.replace('.wav', '.json')
    files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    if meta_file in files:
        cnsc = run_cnsc(transcript, filename)
        print(cnsc)

    # append the cnsc json to the transcript
    return transcript


if __name__ == "__main__":
    transcript = []
    filename = '1.wav'

    cnsc_result = run_cnsc(transcript, filename)
    print(cnsc_result)
