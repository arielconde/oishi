from .cnsc import run_cnsc

def handle_overlaps(transcript, filename):
    cnsc_transcript = run_cnsc(transcript, filename)
    return cnsc_transcript
