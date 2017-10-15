"""
    Process & Improvements to be done:
    DONE - Frame the Signal
    DONE - Apply Preemphasis
    TODO - Apply zero padding to the signal
    TODO - Apply hamming window on each frame
    TODO - Dynamic Number of FFT, base on signal frequency and frame size
    DONE - FFT
    DONE - Power Spectrum
    DONE - Periodigram Power Spectrum
    DONE - Melpoints
    DONE - Create bins
    DONE - Create Filterbank
    DONE - Get each 26 features by multiplying pspec with the filter bank
    DONE - Log of 26 features
    TODO - When using log, avoid zeros "numerical stability"
    DONE - DCT of 26 features
    DONE - Get the features needed, based on nceps = 12
    TODO - Lifter the final mffc
    TODO - Mean normalization (?)
"""

import scipy.io.wavfile as wav
import numpy
from numpy.fft import fft
from scipy.fftpack import dct


def mfcc(frame, rate, NFFT):

    # get periodigram power spectrum
    complex_spectrum = fft(frame, NFFT)
    power_spectrum = (numpy.abs(complex_spectrum)) ** 2
    pspec = power_spectrum * 1 / NFFT

    # power spectrum is symmetrical we only keep have of it
    pspec = pspec[0: int(len(pspec) / 2) + 1]

    # create filter bank
    NFILT = 26
    lowfreq = 0
    highfreq = int(rate / 2)
    lowmel = hz2mel(lowfreq)
    highmel = hz2mel(highfreq)
    melpoints = numpy.linspace(lowmel, highmel, NFILT + 2)
    bin = numpy.floor((NFFT + 1) * mel2hz(melpoints) / rate)

    fbank = numpy.zeros([NFILT, NFFT // 2 + 1])
    for j in range(0, NFILT):
        for i in range(int(bin[j]), int(bin[j + 1])):
            fbank[j, i] = (i - bin[j]) / (bin[j + 1] - bin[j])
        for i in range(int(bin[j + 1]), int(bin[j + 2])):
            fbank[j, i] = (bin[j + 2] - i) / (bin[j + 2] - bin[j + 1])

    # Get the nfilt features
    feats = [0] * NFILT  # Crete array of zeros
    for i in range(0, NFILT):
        feat = 0
        for index, ps in enumerate(pspec):
            feat += ps * fbank[i][index]
        feats[i] = feat

    log_feats = numpy.log(feats)
    dct_feats = dct(log_feats)
    final_mfcc = dct_feats[1:13]  # keep the 2-13 coefficient, num_ceps = 12

    return final_mfcc


def hz2mel(hz):
    return 2595 * numpy.log10(1 + hz / 700)


def mel2hz(mel):
    return 700 * (10**(mel / 2595.0) - 1)


if __name__ == '__main__':
    (rate, signal) = wav.read("english.wav")

    # Apply pre emphasis
    coeff = 0.97
    signal = numpy.append(signal[0], signal[1:] - coeff * signal[:-1])

    # frame the signal
    frame_size = 0.025  # 20ms
    frame_step = 0.01  # 10ms
    samples_per_frame = frame_size * rate
    samples_per_step = frame_step * rate
    num_frames = int(len(signal) / samples_per_step)

    NFFT = 512

    for i in range(1, num_frames):
        frame_index = i
        s = int(samples_per_step * frame_index)
        e = int(s + samples_per_frame)
        frame = signal[s:e]
        feat = mfcc(frame, rate, NFFT)
        print('Frame # %d' % i)
        print(feat)
