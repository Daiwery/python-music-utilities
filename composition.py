"""
Module for working with note sequences.
"""
from typing import Dict, List, Tuple, Any

from midiUtilities import MidiTrack, MidiMessage
from note import Note


class Sequence:
    """
    The note sequence.
    """

    def __init__(self, notes: List[Note], id_track, next_sequences=None, delay: float = 0, start_end: bool = False):
        """
        :param notes: List of notes.
        :param id_track: The track's id, which this sequence belongs.
        :param next_sequences: List of Sequences that come after this sequence.
        :param delay: Delay in musical note duration.
        :param start_end: Delay after the start or end of the previous sequence.
        """
        if next_sequences is None:
            next_sequences = []
        self.notes: List[Note] = notes
        self.id_track = id_track
        self.next_sequences = next_sequences
        self.delay = delay
        self.start_end = start_end

    def toMidi(self) -> (List[MidiMessage], float):
        """
        Converts a list of notes to a list of MidiMessages with
        an absolute time value (relative to the start of the sequence).
        Time in musical note duration.

        :return: Tuple of the form: (List of MidiMessages, sequence's duration).
        """
        messages = []
        global_time = 0
        for i, note in enumerate(self.notes):
            if i == 0:
                global_time = note.delay
            else:
                global_time += note.delay - int(note.start_end) * self.notes[i - 1].duration
            messages.append(MidiMessage("note_on", global_time, note=note.toMidi(), velocity=note.velocity))

            global_time += note.duration
            messages.append(MidiMessage("note_off", global_time, note=note.toMidi(), velocity=note.velocity))

        return messages, global_time

    def compile(self, last_start_time=0, last_end_time=0) -> List[Tuple[str, List[MidiMessage]]]:
        """
        Turns itself and all sequences into a list of tuples of the form: (track, sequence message list).
        This function calls itself recursively, adding data to the final result.

        :param last_start_time: The start time of the past sequence.
        :param last_end_time: The end time of the past sequence.
        :return: List of tuples of the form: (track, sequence message list).
        """
        messages, duration = self.toMidi()

        # start_time - the start time of the current sequence.
        # end_time - the end time of the current sequence.
        if self.start_end:
            start_time = last_start_time + self.delay
        else:
            start_time = last_end_time + self.delay
        end_time = start_time + duration

        for i, message in enumerate(messages):
            messages[i].time += start_time

        results = [(self.id_track, messages)]
        for sequence in self.next_sequences:
            results += sequence.compile(start_time, end_time)

        return results

    def __add__(self, other):
        """
        Adds the sequence to the next_sequence.
        Note that the added sequence is returned.
        """
        if isinstance(other, Sequence):
            self.next_sequences.append(other)
            return other
        raise TypeError("unsupported operand type(s) for +: 'sequence' and '{}'".format(other.__name__))


class Composition:
    """
    The composition.
    """

    def __init__(self):
        # Dictionary of the form: {id_track: midi-instrument number}
        self.tracks: Dict[Any, int] = {}
        # Initial sequences in a composition
        self.initial_sequences: List[Sequence] = []

    def add_track(self, id_track: Any, instrument: int):
        """
        Adds a new track to the composition.

        :param id_track: The track's id.
        :param instrument: midi-instrument number.
        """
        if id_track in self.tracks:
            raise ValueError("The track {} already exists.".format(id_track))
        self.tracks[id_track] = instrument

    def add_sequence(self, sequence: Sequence):
        """
        Adds a new initial sequence to the composition.
        Note that the added sequence is returned.

        :param sequence: The Sequence.
        """
        if sequence.id_track not in self.tracks:
            raise ValueError("The track {} does not exists.".format(sequence.id_track))
        self.initial_sequences.append(sequence)
        return sequence

    def compile(self) -> List[MidiTrack]:
        """
        Compiles the entire composition and returns a list of MidiTracks.

        :return: List of midi-tracks with raw midi-messages..
        """
        # Dictionary of the form: {id_track: MidiTrack}
        tracks = {}
        for track in self.tracks:
            tracks[track] = MidiTrack(track, self.tracks[track])

        for sequence in self.initial_sequences:
            for result in sequence.compile():
                tracks[result[0]].append(result[1])

        return list(tracks.values())
