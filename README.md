# hearSound

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

The default MIDI bus name in `midi.py` is `Python` or `IAC Driver Python`

### Capturing multiple sound devices

https://github.com/spatialaudio/python-sounddevice/issues/154

## Run Commands

To see all command-line arguments:

```shell
poetry run python src/dft_pitch.py -h
```

To run `src/dft_pitch.py`

```shell
poetry run python src/dft_pitch.py
```
