from python_speech_features import mfcc, sigproc
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture as GMM
import numpy as np
import sounddevice as sd
import seaborn as sns
sns.set()


def filter_signal(signal):
    lowpass_val = 2500
    signal[np.where(abs(signal) < lowpass_val)] = 0


def get_min_n_components(feats, min=1, max=20,
                         covariance_type='full', criteria='BIC'):
    n_components = np.arange(min, max)
    models = [GMM(n, covariance_type='full', random_state=0).fit(feats)
              for n in n_components]
    if criteria == 'AIC':
        aics = [m.aic(feats) for m in models]
        return np.argmin(aics)
    else:
        bics = [m.bic(feats) for m in models]
        return np.argmin(bics)


def run():
    rate, signal = wav.read("../recordings/english.wav")
    sigproc.preemphasis(signal)
    # filter_signal(signal)

    frame_size = 0.02  # second
    frame_step = 0.01  # second

    mfcc_feat = mfcc(signal, rate, winlen=frame_size,
                     winstep=frame_step)

    n_components = 2
    n_components = get_min_n_components(mfcc_feat)
    print("No. of identified components: {0}".format(n_components))
    gmm = GMM(n_components=n_components, covariance_type='full')
    labels = gmm.fit(mfcc_feat).predict(mfcc_feat)

    plt.scatter(mfcc_feat[:, 0], mfcc_feat[:, 1], c=labels)
    plt.show()

    plt.plot(signal)
    plt.show()

def hello():
    return "Welp"


if __name__ == "__main__":
    run()
