import mido
from time import sleep
from scipy.signal import medfilt
import random

print(mido.get_output_names())


C = 60
G = 55
A = 57
F = 53

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def midi_number_to_note(number):
    octave = number // len(NOTES) - 1
    note = NOTES[number % len(NOTES)]
    return note + str(octave)


# some example using mido from
# https://natespilman.com/blog/playing-chords-with-mido-and-python/
def note(note, velocity=64, time=2):
    """
    note: midi note
    velocity: "how fast the note was struck or released" - dynamic
    channel: 0..15
    time: "not included in the encoded message"
    """
    message = mido.Message("note_on", note=note, velocity=velocity, time=time)
    return message


def note_off(note, velocity=64, time=2):
    return mido.Message("note_off", note=note, velocity=velocity, time=time)


def major_chord(root, outport, velocity=64, duration=0.2):
    """Major chord from the root note"""
    if root + 7 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 4, velocity))
    outport.send(note(root + 7, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 4, velocity))
    outport.send(note_off(root + 7, velocity))


def minor_chord(root, outport, velocity=64, duration=0.2):
    """Minor chord based on the root node"""
    if root + 7 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 3, velocity))
    outport.send(note(root + 7, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 3, velocity))
    outport.send(note_off(root + 7, velocity))


def major_seventh(root, outport, velocity=64, duration=0.2):
    """Major seventh chord based on root node"""
    if root + 11 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 4, velocity))
    outport.send(note(root + 7, velocity))
    outport.send(note(root + 11, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 4, velocity))
    outport.send(note_off(root + 7, velocity))
    outport.send(note_off(root + 11, velocity))


def minor_seventh(root, outport, velocity=64, duration=0.2):
    """Minor seventh chord based on root node"""
    if root + 10 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 3, velocity))
    outport.send(note(root + 7, velocity))
    outport.send(note(root + 10, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 3, velocity))
    outport.send(note_off(root + 7, velocity))
    outport.send(note_off(root + 10, velocity))


def dom_seventh(root, outport, velocity=64, duration=0.2):
    """Dominate seventh chord based on root node"""
    if root + 10 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 4, velocity))
    outport.send(note(root + 7, velocity))
    outport.send(note(root + 10, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 4, velocity))
    outport.send(note_off(root + 7, velocity))
    outport.send(note_off(root + 10, velocity))


def dim_seventh(root, outport, velocity=64, duration=0.2):
    """diminished seventh chord based on root node"""
    if root + 9 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 3, velocity))
    outport.send(note(root + 6, velocity))
    outport.send(note(root + 9, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 3, velocity))
    outport.send(note_off(root + 6, velocity))
    outport.send(note_off(root + 9, velocity))


def half_dim_seventh(root, outport, velocity=64, duration=0.2):
    """half diminished seventh chord based on root node"""
    if root + 10 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 3, velocity))
    outport.send(note(root + 6, velocity))
    outport.send(note(root + 10, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 3, velocity))
    outport.send(note_off(root + 6, velocity))
    outport.send(note_off(root + 10, velocity))


def aug_seventh(root, outport, velocity=64, duration=0.2):
    """augmented seventh chord based on root node"""
    if root + 11 > 127:
        return
    outport.send(note(root, velocity))
    outport.send(note(root + 4, velocity))
    outport.send(note(root + 8, velocity))
    outport.send(note(root + 11, velocity))
    sleep(duration)
    outport.send(note_off(root, velocity))
    outport.send(note_off(root + 4, velocity))
    outport.send(note_off(root + 8, velocity))
    outport.send(note_off(root + 11, velocity))


def fifths(root, outport, velocity=64, duration=0.2):
    """Stacking fifths harmony that are aboved the root note"""
    for i in range(25):
        if root + i * 7 > 127:
            break
        outport.send(note(root + i * 7, velocity))
    sleep(duration)
    for i in range(25):
        if root + i * 7 > 127:
            break
        outport.send(note_off(root + i * 7, velocity))


def fifth_scale(root, outport, velocity=64, duration=0.1):
    """Stacking fifths scale that are aboved the root note"""
    for i in range(25):
        if root + i * 7 > 127:
            break
        outport.send(note(root + i * 7, velocity))
        sleep(0.1)
        outport.send(note_off(root + i * 7, velocity))


def fourths(root, outport, velocity=64, duration=0.2):
    """Stacking fourths harmony that are aboved the root note"""
    for i in range(25):
        if root + i * 5 > 127:
            break
        outport.send(note(root + i * 5, velocity))
    sleep(duration)
    for i in range(25):
        if root + i * 5 > 127:
            break
        outport.send(note_off(root + i * 5, velocity))


def fourth_scale(root, outport, velocity=64, duration=0.1):
    """Stacking fourths scale that are aboved the root note"""
    for i in range(25):
        if root + i * 5 > 127:
            break
        outport.send(note(root + i * 5, velocity))
        sleep(random.randint(1, 10)/100)
        outport.send(note_off(root + i * 5, velocity))


def fourth_scale_down(root, outport, velocity=64, duration=0.1):
    """Downward fourths scale that are aboved the root note"""
    for i in range(25):
        if root - i * 5 < 0:
            break
        outport.send(note(root - i * 5, velocity))
        sleep(random.randint(1, 10)/100)
        # outport.send(note_off(root - i * 5, velocity))
        sleep(random.randint(1, 30)/100)


def fifth_scale_down(root, outport, velocity=64, duration=0.1):
    """Stacking fifths scale that are aboved the root note"""
    for i in range(25):
        if root - i * 7 < 0:
            break
        outport.send(note(root - i * 7, velocity))
        sleep(random.randint(1, 10)/100)
        outport.send(note_off(root - i * 7, velocity))
        sleep(random.randint(1, 20)/100)


# def triad_octave(root, outport, velocity=64, duration=0.1):
#     for i in range(10):
#         if root - i * 7 - 5 < 0:
#             break
#         # dom_seventh(root + i * 12, velocity)
#         outport.send(note(root - i * 7, velocity))
#         sleep(random.randint(1, 10)/100)
#         outport.send(note(root - i * 7, velocity))
#         sleep(random.randint(1, 10)/100)
#         outport.send(note(root - i * 7 - 5, velocity))
#         sleep(random.randint(1, 10)/100)
#         outport.send(note(root - i * 7 - 5, velocity))
#         sleep(0.2)
        # sleep(random.randint(1, 10)/100)
        # outport.send(note_off(root + i * 7, velocity))

# while True:
#     major_chord(C, 1)
#     major_chord(G, 1)
#     minor_chord(A, 1)
#     major_chord(F, 1)
#     major_chord(F, 1)
#     major_chord(G, 1)
#     major_chord(C, 2)


def play(root, outport, velocity=64, duration=3):
    # if root % 2 == 1:
    #     # fourth_scale_down(root, velocity)
    #     # minor_chord(root, velocity, duration)
    #     fourth_scale(root, velocity)
    #     # fourths(root, velocity)
    # else:
    #     major_seventh(root, velocity, duration)
    #     sleep(0.1)
    #     minor_seventh(root + 14, velocity, duration)
    #     sleep(0.15)
    #     major_seventh(root + 7, velocity, duration)
    #     sleep(0.1)
    #     fifths(root, velocity, duration)
    #     fifth_scale(root, velocity)
    #     fifth_scale(root, velocity, duration)
    outport.send(note(root, velocity))
    if duration < 2:
        duration = 2
    print(duration)
    sleep(duration)
    outport.send(note_off(root, velocity))
    # fourth_scale(root, velocity, duration)
    # triad_octave(root, velocity)


# midi to note example from https://github.com/justinsalamon/
# audio_to_midi_melodia/blob/master/audio_to_midi_melodia.py
def midi_to_notes(midi, fs, hop, smooth, minduration):

    # smooth midi pitch sequence first
    if smooth > 0:
        filter_duration = smooth  # in seconds
        filter_size = int(filter_duration * fs / float(hop))
        if filter_size % 2 == 0:
            filter_size += 1
        midi_filt = medfilt(midi, filter_size)
    else:
        midi_filt = midi
    # print(len(midi),len(midi_filt))

    notes = []
    p_prev = None
    duration = 0
    onset = 0
    for n, p in enumerate(midi_filt):
        if p == p_prev:
            duration += 1
        else:
            # treat 0 as silence
            if p_prev > 0:
                # add note
                duration_sec = duration * hop / float(fs)
                # only add notes that are long enough
                if duration_sec >= minduration:
                    onset_sec = onset * hop / float(fs)
                    notes.append((onset_sec, duration_sec, p_prev))

            # start new note
            onset = n
            duration = 1
            p_prev = p
