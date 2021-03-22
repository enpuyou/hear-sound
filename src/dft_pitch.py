#!/usr/bin/env python3
# inspired and modified based on https://devpost.com/software/pitch-detection
import sys
import numpy as np
import time
import math

from midi import play, midi_number_to_note
from threading import Lock

from scipy.signal import blackmanharris
from scipy.signal import find_peaks

import threading

buf = np.zeros(1)  # Microphone data buffer
lock = Lock()  # Buffer lock
fresh_data = True  # Flag to indicate if new data is available
args = ""
outport = ""


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
    global norm
    norm = np.linalg.norm(indata)
    volume_norm = int(np.linalg.norm(indata) * 10)


def compute_pitch(arg, out):
    """
    Computes the current pitch of the signal in a loop until program
    termination.
    """
    global buf
    global bin_value
    global fresh_data
    global args
    global outport
    args = arg
    outport = out
    avg_size = 2
    sq12_2 = 1.05946309
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
        # print(max(fft)/norm)
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

            # print(note_ind)
            # Remove noise and frequencies that are too low to be interesting
            if (np.average(fft) > args.noise_threshold) and last_freq > 40:
                if args.repeat_count < 1 or same_count == args.repeat_count:
                    midinote = int(69 + 12 * math.log2(last_freq / 440))
                    note_name = midi_number_to_note(midinote)
                    print(f"Pitch: {note_name} ({last_freq} Hz)")

                    thread = threading.Thread(
                        target=play, args=(midinote, outport, int(velocity))
                    )
                    thread.start()


def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(volume_norm)


# if __name__ == "__main__":
#     global args
#     args, parser = parse(sys.argv[1:])
#     try:
#         if args.list_devices:
#             print(sd.query_devices())
#             parser.exit(0)
#         print(args.device)
#         stream = sd.InputStream(
#             device=args.device,
#             channels=args.channels,
#             samplerate=args.samplerate,
#             callback=audio_callback,
#         )
#         with stream:
#             compute_pitch()
#         # for d in range(len(args.device)):
#         #     pitch_thread = threading.Thread(target=stream, args=(args, d))
#         #     pitch_thread.start()

#     except Exception as e:
#         parser.exit(type(e).__name__ + ": " + str(e))
