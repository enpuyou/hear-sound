import argparse


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def parse(args):
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
    arguments = parser.parse_args(args)
    return arguments
