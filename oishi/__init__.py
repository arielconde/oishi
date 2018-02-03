import os
import numpy as np
import soundfile as sf
from python_speech_features import mfcc, sigproc
from sklearn.mixture import GaussianMixture as GMM
from collections import Counter
import random
from .transcription import transcribe_gcs_with_word_time_offsets
from .oh import handle_overlaps

"""
Folder contains the transcripts from API
Transcripts are kept to save on Request Limit
"""
API_TRANSCRIPTS_FOLDER = 'oishi/' + 'api_transcripts/'
AUDIO_FOLDER = 'uploads/'


"""
Diarize function return a dict transcript of the given audio file
"""


def diarize(filename):
    audio_filename = filename
    audio_path = AUDIO_FOLDER + audio_filename
    transcript_filename = filename.replace("wav", "txt")
    transcript_path = API_TRANSCRIPTS_FOLDER + transcript_filename

    if os.path.exists(transcript_path):
        transcript = run_diarization(audio_path, audio_filename, transcript_path)
        return {
            'filename': audio_filename,
            'transcript_file': transcript_filename,
            'transcript': transcript
        }
    else:
        print("Creating a new file")
        # Create script to upload to GCS
        uri = "gs://oishi_storage/audio/RealisticFilm1.wav"
        transcription.transcribe_gcs_with_word_time_offsets(uri)
    return {'trascript': 'Hello'}


def run_diarization(audio_path, audio_filename, transcript_path):
    (sig, rate) = sf.read(audio_path)

    # Measure in seconds
    frame_size = 0.020
    frame_step = 0.010

    samples_per_frame = frame_size * rate
    samples_per_step = frame_step * rate

    # Frame signal to use for processing
    framed_signal = sigproc.framesig(sig, samples_per_frame,
                                     samples_per_step)

    """
    Get the power spectrum of each frame
    Voiced segments in signal has higher power spectrum
    """
    power_spec = sigproc.powspec(framed_signal, 2048)
    power_spec_total = np.sum(power_spec, axis=1)

    """
    Get the voiced segments
    """
    VOICED_THRESHOLD = 0.0200  # Experimental value, varies on input
    voiced_idxs = np.where(power_spec_total > VOICED_THRESHOLD)
    voiced_idxs = voiced_idxs[0]

    """
    Get the MFCC per frame of the signal
    """
    mfcc_feat = mfcc(sig, rate, winlen=frame_size,
                     winstep=frame_step, nfft=1024)

    """
    Create a GMM
    Fit the MFCC Features on with GMM then get the labels
    """
    N_SPEAKERS = 3
    gmm = GMM(n_components=N_SPEAKERS, covariance_type='full', random_state=3)
    labels = gmm.fit(mfcc_feat[voiced_idxs]).predict(mfcc_feat[voiced_idxs])

    transcript = []

    with open(transcript_path) as transcript_file:
        for line in transcript_file:
            if 'Waiting for operation to complete...' in line:
                continue
            if 'Transcript:' in line or 'Confidence:' in line:
                continue
            tokens = [token.split(':') for token in line.replace(
                " ", "").strip().split(',')]
            word = tokens[0][1]
            start_time = tokens[1][1]
            end_time = tokens[2][1]
            start_idx = int(float(start_time) * 100)
            end_idx = int(float(end_time) * 100)
            if start_idx == end_idx:
                start_idx -= 1
                end_idx += 1

            idxs_s = np.where((voiced_idxs >= start_idx)
                              & (voiced_idxs <= end_idx))

            counter_labels = Counter(labels[idxs_s])
            if idxs_s[0].size == 0:
                continue

            label = counter_labels.most_common(1)[0][0]
            turn = {
                'is_overlapping': False,
                'speaker_id': str(label),
                'word': word,
                'start_time': start_time,
                'end_time': end_time,
                'hasWord': True
            }

            transcript.append(turn)

    return handle_overlaps(transcript, audio_filename)



if __name__ == "__main__":
    diarize('1.wav')