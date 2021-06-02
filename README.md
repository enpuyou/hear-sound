# hear-sound

## Install dependencies

```shell
poetry install
```

Before install PyAudio:

```shell
brew install portaudio
```

Set up virtual MIDI bus:

https://help.ableton.com/hc/en-us/articles/209774225-How-to-setup-a-virtual-MIDI-bus

### Installation of `pocketsphinx` on Big Sur

https://github.com/bambocher/pocketsphinx-python/issues/67

https://cmusphinx.github.io/wiki/download/

#### Tuning parameters

https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst

### Virtual MIDI bus

There is currently no default MIDI bus name in the project. User will need to provide
through the command line argument

### Capturing multiple sound devices

https://github.com/spatialaudio/python-sounddevice/issues/154

## Run Commands

To see all command-line arguments:

```shell
poetry run python src/main.py -h
```

To see all devices and virtual MIDI buses that are available:

```shell
poetry run python src/main.py -l
```

A sample output on my machine:

```sh
Sound devices:
>  0 AirPods, Core Audio (1 in, 0 out)
   1 AirPods, Core Audio (0 in, 2 out)
   2 BlackHole 16ch, Core Audio (16 in, 16 out)
   3 BlackHole 2ch, Core Audio (2 in, 2 out)
   4 MacBook Pro Microphone, Core Audio (1 in, 0 out)
<  5 MacBook Pro Speakers, Core Audio (0 in, 2 out)
   6 ZoomAudioDevice, Core Audio (2 in, 2 out)
   7 in mac + B2 program, Core Audio (3 in, 2 out)
   8 in mac + B16 video, Core Audio (17 in, 16 out)
   9 out mac + B16 daw, Core Audio (0 in, 2 out)
  10 out mac + B2 video, Core Audio (0 in, 2 out)
Virtual MIDI Buses:
   0 IAC Driver Bus 0
   1 IAC Driver Bus 1
```

To run `src/main.py` with `device 4` and `bus 0`:

```shell
poetry run python src/main.py -d 4 -u 0
```

Or to run multiple devices, for example, with `device 0`, `device 4` and `bus 0`, `bus 1`:

```shell
poetry run python src/main.py -d 0 4 -u 0 1
```

The output of `device 0` will then send to the `bus 0`, `device 4` will send to `bus 1`
