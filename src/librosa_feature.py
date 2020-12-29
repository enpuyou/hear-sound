import librosa
import librosa.display
import numpy as np

import matplotlib.pyplot as plt

path = "resources/no-god.wav"

# Load the audio as a waveform `y` - time series floating point array
# Store the sampling rate as `sr` - number of samples per second of audio
y, sr = librosa.load(path)

# an estimate of the tempo (in beats per minute)
# an array of frame numbers corresponding to detected beat events
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

#  an array of timestamps (in seconds) corresponding to detected beat events
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Separate harmonics and percussives into two waveforms
# separated into two time series, containing the harmonic (tonal) and
# percussive (transient) portions of the signal.
y_harmonic, y_percussive = librosa.effects.hpss(y)

# Beat track on the percussive signal
# tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)

# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length = 512

# Compute MFCC features from the raw signal
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)

# And the first-order differences (delta features)
mfcc_delta = librosa.feature.delta(mfcc)

# Stack and synchronize between beat events
# This time, we'll use the mean value (default) instead of median
beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),
                                    beat_frames)

# Compute chroma features from the harmonic signal
chromagram = librosa.feature.chroma_cqt(y=y_harmonic,
                                        sr=sr)

# Aggregate chroma features between beat events
# We'll use the median value of each feature between beat frames
beat_chroma = librosa.util.sync(chromagram,
                                beat_frames,
                                aggregate=np.median)

# Finally, stack all beat-synchronous features together
beat_features = np.vstack([beat_chroma, beat_mfcc_delta])


plt.figure(figsize=(12, 5))
librosa.display.waveplot(y, sr)
for bt in beat_times:
    plt.axvline(x=bt)
plt.show()
