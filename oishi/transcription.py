import pprint

# Function Declaration
def transcribe_gcs_with_word_time_offsets(gcs_uri):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        # encoding=enums.RecognitionConfig.AudioEncoding.FLAC, # encoding is optional for WAV Files
        # sample_rate_hertz=16000, # sample_rate is optional for WAV Files
        language_code='en-PH',
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=90)

    for result in result.results:
        alternative = result.alternatives[0]
        print('Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))
    return result


if __name__ == "__main__":

    # Audio files are upload to google cloud storage

    uri = "gs://oishi_storage/audio/RealisticFilm1.wav"
    transcribe_gcs_with_word_time_offsets(uri)
