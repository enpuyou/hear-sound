import mido
from time import sleep

midibus_name = "Python"

# repeating C
# middleC = 60
# while True:
#     msg = mido.Message('note_on', note=middleC, velocity=64)
#     outport = mido.open_output(f'IAC Driver {midibus_name}')
#     outport.send(msg)
#     sleep(.5)

# some example using mido from https://natespilman.com/blog/playing-chords-with-mido-and-python/
def note(note, velocity=64, time=2):
    return mido.Message("note_on", note=note, velocity=velocity, time=time)


def note_off(note, velocity=64, time=2):
    return mido.Message("note_off", note=note, velocity=velocity, time=time)


outport = mido.open_output(f'IAC Driver {midibus_name}')


def major_chord(root, duration):
    outport.send(note(root))
    outport.send(note(root + 4))
    outport.send(note(root + 7))
    sleep(duration)
    outport.send(note_off(root))
    outport.send(note_off(root + 4))
    outport.send(note_off(root + 7))


def minor_chord(root, duration):
    outport.send(note(root))
    outport.send(note(root + 3))
    outport.send(note(root + 7))
    sleep(duration)
    outport.send(note_off(root))
    outport.send(note_off(root + 3))
    outport.send(note_off(root + 7))


C = 60
G = 55
A = 57
F = 53

while True:
    major_chord(C, 1)
    major_chord(G, 1)
    minor_chord(A, 1)
    major_chord(F, 1)
    major_chord(F, 1)
    major_chord(G, 1)
    major_chord(C, 2)
