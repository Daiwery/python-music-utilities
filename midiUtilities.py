"""
Module for working with midi-messages and files based mido module.
"""
import os.path
from typing import List

import mido


class MidiMessage:
    """
    Represents a midi-message.
    """

    def __init__(self, kind: str, time: float, **kwargs):
        self.kind = kind
        # Time can to have different dimension and essence depending on context.
        self.time = time
        # Magic hack for mido.Message arguments.
        self.kwargs = kwargs

    def toMido(self) -> mido.Message:
        """
        Transforms himself in midi-message.

        :return: mido.Message corresponding to this message
        """
        return mido.Message(type=self.kind, time=self.time, **self.kwargs)

    def __eq__(self, other):
        if isinstance(other, MidiMessage):
            return self.kind == other.kind and self.time == other.time and self.kwargs == other.kwargs
        return False

    def __str__(self):
        return str({"kind": self.kind, "time": self.time, "kwargs": self.kwargs})

    __repr__ = __str__



class MidiTrack:
    """
    Represents a one midi-track.
    """

    def __init__(self, label: str, instrument: int, messages: List[MidiMessage] = None):
        """
        :param label: Name of track.
        :param instrument: Instrument that is played in this track.
        :param messages: List of midi-messages.
        """
        if messages is None:
            messages = []
        self.messages = messages
        self.label = label
        self.instrument = instrument

    def append(self, messages: List[MidiMessage]):
        """
        Appends list of midi-messages in track.

        :param messages: List of midi-messages.
        """
        self.messages += messages

    def toMido(self):
        """
        Transforms himself in mido.MidiTrack.

        :return: mido.MidiTrack corresponding to this track.
        """
        track = mido.MidiTrack()
        # track.append(mido.MetaMessage(mido.MetaMessage('track_name', name=self.label)))
        track.append(mido.Message(type="program_change", program=self.instrument, time=0))
        for message in self.messages:
            track.append(message.toMido())
        return track


def transform_time(messages: List[MidiMessage], bmp: int | float,
                   ticks_per_beat: int = 480, to_tick: bool = True) -> List[MidiMessage]:
    """
    Transforms raw midi-messages to midi-message with the necessary time’s attributes.

    :param messages: List of raw midi-messages.
    :param bmp: Number of metronome beats per minute (= number of quarter notes per minute).
    :param ticks_per_beat: Number of ticks per beat. Specifies the degree of sampling.
    :param to_tick: Convert to ticks or seconds.
    :return: List of midi-message with the necessary time’s attributes.
    """
    messages.sort(key=lambda x: x.time)

    # Convert from absolute time to relative time.
    global_time = 0
    for i, message in enumerate(messages):
        time = message.time - global_time
        global_time = message.time

        messages[i].time = time

    for i, message in enumerate(messages):
        # Transform to seconds.
        messages[i].time /= bmp / (4 * 60)
        if to_tick:
            # Transform to ticks.
            messages[i].time = int(
                mido.second2tick(messages[i].time, ticks_per_beat=ticks_per_beat, tempo=1 / (bmp / 60) * 10 ** 6))

    return messages


def write_to_file(tracks: List[MidiTrack], path: str, bmp: int, ticks_per_beat: int = 480):
    """
    Writes each track to a separate midi-file.
    Performs necessary transformations before recording.

    :param tracks: List of midi-tracks.
    :param path: The directory for files.
    :param bmp: Number of metronome beats per minute (= number of quarter notes per minute).
    :param ticks_per_beat: Number of ticks per beat. Specifies the degree of sampling.
    """
    for i, track in enumerate(tracks):
        tracks[i].messages = transform_time(track.messages, bmp=bmp, ticks_per_beat=ticks_per_beat)
    for track in tracks:
        midi = mido.MidiFile()
        midi.tracks.append(track.toMido())
        midi.save(os.path.join(path, track.label + ".midi"))
