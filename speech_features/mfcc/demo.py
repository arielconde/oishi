# Runs mfcc on a single frame of the input signal

import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy
from numpy.fft import fft
from scipy.fftpack import dct


def run():

    (rate, signal) = wav.read("english.wav")

    PLT_COUNT = 10
    plt.subplot(PLT_COUNT, 1, 1)
    plt.plot(signal)

    # Apply pre emphasis
    coeff = 0.97
    signal = numpy.append(signal[0], signal[1:] - coeff * signal[:-1])

    plt.subplot(PLT_COUNT, 1, 2)
    plt.plot(signal)

    # frame the signal
    frame_size = 0.025  # 20ms
    frame_step = 0.01  # 10ms
    samples_per_frame = frame_size * rate
    samples_per_step = frame_step * rate
    num_frames = int(len(signal) / frame_step)

    frame_index = 1
    s = int(samples_per_step * frame_index)
    e = int(s + samples_per_frame)
    frame = signal[s:e]

    plt.subplot(PLT_COUNT, 1, 3)
    plt.plot(frame)

    NFFT = 512

    # get periodigram power spectrum
    complex_spectrum = fft(frame, NFFT)
    power_spectrum = (numpy.abs(complex_spectrum)) ** 2
    pspec = power_spectrum * 1 / NFFT

    plt.subplot(PLT_COUNT, 1, 4)
    plt.plot(pspec)

    # power spectrum is symmetrical we only keep have of it
    pspec = pspec[0: int(len(pspec) / 2) + 1]
    len_pspec = len(pspec)

    plt.subplot(PLT_COUNT, 1, 5)
    plt.plot(pspec)

    # create filter bank
    NFILT = 26
    lowfreq = 0
    highfreq = int(rate / 2)
    lowmel = hz2mel(lowfreq)
    highmel = hz2mel(highfreq)
    melpoints = numpy.linspace(lowmel, highmel, NFILT + 2)
    bin = numpy.floor((NFFT + 1) * mel2hz(melpoints) / rate)

    # Create Filterbank
    fbank = numpy.zeros([NFILT, NFFT // 2 + 1])
    for j in range(0, NFILT):
        for i in range(int(bin[j]), int(bin[j + 1])):
            fbank[j, i] = (i - bin[j]) / (bin[j + 1] - bin[j])
        for i in range(int(bin[j + 1]), int(bin[j + 2])):
            fbank[j, i] = (bin[j + 2] - i) / (bin[j + 2] - bin[j + 1])

    plt.subplot(PLT_COUNT, 1, 6)
    plt.plot(fbank.T)  # matrix transpose of bank

    # Get the nfilt features
    feats = [0] * NFILT
    for i in range(0, NFILT):
        feat = 0
        for index, ps in enumerate(pspec):
            feat += ps * fbank[i][index]
        feats[i] = feat

    plt.subplot(PLT_COUNT, 1, 7)
    plt.plot(feats)

    log_feats = numpy.log(feats)

    plt.subplot(PLT_COUNT, 1, 8)
    plt.plot(log_feats)

    dct_feats = dct(log_feats)[:13]

    plt.subplot(PLT_COUNT, 1, 9)
    plt.plot(dct_feats)

    final_mfcc = dct_feats[1:13] # keep the 2-13 coefficient, num_ceps = 12
    plt.subplot(PLT_COUNT, 1, 10)
    plt.plot(final_mfcc)

    print('Final coefficients\n', final_mfcc)

    plt.show()


def hz2mel(hz):
    return 2595 * numpy.log10(1 + hz / 700)


def mel2hz(mel):
    return 700 * (10**(mel / 2595.0) - 1)


if __name__ == '__main__':
    run()
