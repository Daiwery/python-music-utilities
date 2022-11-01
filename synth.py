"""
Module for playing notes in real time based fluidsynth.
"""
from time import sleep
from typing import List

import fluidsynth

from midiUtilities import MidiTrack, transform_time


def synth(tracks: List[MidiTrack], bmp: int, sound_font: str, loop: bool = True):
    """
    Playing notes in real time using fluidsynth..

    :param tracks: List of MidiTracks with raw midi-messages..
    :param bmp: Number of metronome beats per minute (= number of quarter notes per minute).
    :param sound_font: The path to the sound font.
    :param loop: Play endlessly or not.
    """
    # Combines all messages into one track without losing track information.
    messages = []
    for i, track in enumerate(tracks):
        for message in track.messages:
            message.kwargs["track"] = i
            messages.append(message)

    messages = transform_time(messages, bmp=bmp, to_tick=False)

    fs = fluidsynth.Synth()
    fs.start()
    font = fs.sfload(sound_font)

    for i, track in enumerate(tracks):
        fs.program_select(i, font, 0, track.instrument)

    while True:
        for message in messages:
            # All magic in waiting necessary time.
            sleep(message.time)

            if message.kind == "note_on":
                fs.noteon(message.kwargs["track"], key=message.kwargs["note"], vel=message.kwargs["velocity"])

            if message.kind == "note_off":
                fs.noteoff(message.kwargs["track"], key=message.kwargs["note"])

        if not loop:
            break
