#!/usr/bin/env python3
# inspired and modified based on https://devpost.com/software/pitch-detection

import argparse
import queue
import sys
import numpy as np
import sounddevice as sd
import time

from threading import Lock

from scipy.signal import blackmanharris
from scipy.signal import find_peaks

import mido

outport = mido.open_output(f"IAC Driver Python")


def note(note, velocity=64, time=10):
    return mido.Message("note_on", note=note, velocity=velocity, time=time)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-l",
    "--list-devices",
    action="store_true",
    help="show list of audio devices and exit",
)
parser.add_argument(
    "-b",
    "--bin-value",
    type=float,
    default=5,
    help="target value in Hertz of a DFT bin",
)
parser.add_argument(
    "-n",
    "--noise-threshold",
    type=float,
    default=0.2,
    help="threshold to differentiate data from noise",
)
parser.add_argument(
    "-p",
    "--peak-threshold",
    type=float,
    default=3 / 5,
    help="threshold to find peaks in the DFT",
)
parser.add_argument(
    "-rc",
    "--repeat-count",
    type=int,
    default=2,
    help="number of times the same note must be repeated to not be considered as noise",
)
parser.add_argument(
    "-d", "--device", type=int_or_str, help="input device (numeric ID or substring)"
)
parser.add_argument(
    "-r",
    "--samplerate",
    type=float,
    default=16000,
    help="sampling rate of audio device",
)
args = parser.parse_args()

buf = np.zeros(1)  # Microphone data buffer
lock = Lock()  # Buffer lock
fresh_data = True  # Flag to indicate if new data is available


def audio_callback(indata, frames, time, status):
    """
    Sounddevice callback that passes the microphone data.
    This function stores it in the global variable buf
    It obtains audio data from the input channels and
    simply forwards everything to the output channels
    """
    if status:
        print(status, file=sys.stderr)

    global fresh_data
    global buf
    lock.acquire()
    fresh_data = True
    bv = args.samplerate / len(indata)
    factor = int(np.max([1, np.ceil(bv / args.bin_value)]))
    if len(buf) == 1:
        buf = np.zeros(factor * len(indata))
        print("Samplerate is: " + str(args.samplerate))
        print("Bin value is: " + str(args.samplerate / len(buf)))

    buf[: (factor - 1) * len(indata)] = buf[len(indata) :]
    buf[(factor - 1) * len(indata) :] = (indata.reshape((len(indata))))[:]
    lock.release()
    global volume_norm
    volume_norm = int(np.linalg.norm(indata)*10)


def compute_pitch():
    """
    Computes the current pitch of the signal in a loop until program
    termination.
    """
    global buf
    global bin_value
    global fresh_data
    avg_size = 2
    sq12_2 = 1.05946309
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    time.sleep(0.2)
    last_note = 0
    last_freq = 0
    same_count = 0
    window_function = np.zeros(1)
    while True:
        # Wait for fresh data in case it is not ready yet
        while not fresh_data:
            time.sleep(0.001)

        # Acquire new data
        lock.acquire()
        buf2 = np.array(buf)
        fresh_data = False
        lock.release()

        # Signal windowing
        if len(window_function) != len(buf2):
            window_function = blackmanharris(len(buf2))
        buf2 = buf2 * window_function

        # Add a bandpass filter ?

        # Compute FFT and limit the maximum frequency
        bin_value = args.samplerate / len(buf2)
        max_ind = int(20000 / bin_value)
        fft = abs(np.fft.fft(buf2))
        if max_ind < len(fft):
            fft = fft[1:max_ind]

        # compute amplitude
        # amplitudes = 2 / args.samplerate * np.abs(fft)
        velocity = volume_norm * 10
        # print(velocity)
        if velocity > 127:
            velocity = 127
        # velocity = np.sqrt(
        #                 np.float_power(fft.real, 2)
        #                 + np.float_power(fft.imag, 2)
        #             )
        # print(velocity)
        # velocity = min(int(127 * (velocity / bin_value)), 127)

        # Compute a mean of the neighboring FFT bins
        acc = 0
        avg_sum = 0
        max_value = np.max(fft)
        center = -1
        idx = 0

        # Find peak

        # while center < 0 and idx < len(fft):
        #     if fft[idx] > (args.peak_threshold * max_value):
        #         center = idx
        #     idx += 1

        peaks = find_peaks(fft, args.peak_threshold * max_value, None, 40 / bin_value)
        if len(peaks[0]) > 0:
            center = peaks[0][0]

        if center >= 0:
            for i in range(-avg_size, avg_size + 1):
                if center + i < len(fft):
                    acc += (center + i) * bin_value * fft[center + i]
                    avg_sum += fft[center + i]

            # Find the note associated to the frequency
            note_ind = int(np.rint((np.log(acc / avg_sum / 440) / np.log(sq12_2)))) % 12
            if note_ind < 0:
                note_ind += 12

            # Determine if the new note is the same as the last one
            if note_ind == last_note and np.abs((acc / avg_sum) / last_freq - 1) < 0.2:
                same_count += 1
            else:
                same_count = 0

            last_note = note_ind
            last_freq = acc / avg_sum

            # Remove noise and frequencies that are too low to be interesting
            if (np.average(fft) > args.noise_threshold) and last_freq > 40:
                if args.repeat_count < 1 or same_count == args.repeat_count:
                    print("Pitch: " + notes[note_ind] + " (" + str(last_freq) + " Hz)")
                    import math

                    midinote = 69 + 12 * math.log2(last_freq / 440)
                    outport.send(note(int(midinote), int(velocity)))


def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print(volume_norm)


if __name__ == '__main__':
    try:
        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)

        # low level stream
        """
        callback (callable, optional) – User-supplied function to consume,
        process or generate audio data in response to requests from an active
        stream. When a stream is running, PortAudio calls the stream callback
        periodically. The callback function is responsible for processing and
        filling input and output buffers, respectively.

        If no callback is given, the stream will be opened in
        “blocking read/write” mode. In blocking mode, the client can receive
        sample data using read() and write sample data using write(), the
        number of frames that may be read or written without blocking is
        returned by read_available and write_available, respectively.

        The callback must have this signature:

        callback(indata: ndarray, outdata: ndarray, frames: int,
                time: CData, status: CallbackFlags) -> None
        The first and second argument are the input and output buffer,
        respectively, as two-dimensional numpy.ndarray with one column per
        channel (i.e. with a shape of (frames, channels)) and with a data type
        specified by dtype. The output buffer contains uninitialized data and
        the callback is supposed to fill it with proper audio data. If no data
        is available, the buffer should be filled with zeros
        (e.g. by using outdata.fill(0)).
        """
        stream = sd.InputStream(
            device=args.device,
            channels=1,
            samplerate=args.samplerate,
            callback=audio_callback,
        )

        with stream:
            compute_pitch()

    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))
