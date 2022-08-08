import re
from typing import List, Union

from note import NOTES, Note, BasicNote


class PianoChord:
    """
    The piano chord.
    """

    def __init__(self, chord: str, octave: int = 3, is_sorted: bool = True, is_normalized: bool = True):
        """
        Currently only minor and major chords are available.

        @param chord: For example, Cm, D#, etc.
        @param octave: The octave number on which the tonic is located.
        @param is_sorted: Sort or not.
        @param is_normalized: Normalize or not.
        """
        keys = re.split("(m)", chord)

        self.tonic: BasicNote = BasicNote(NOTES[keys[0]], octave)

        self.notes: List[BasicNote] = [self.tonic, self.tonic + 4, self.tonic + 7]
        if len(keys) > 1:
            if keys[1] == "m":
                self.notes[1] -= 1

        if is_sorted:
            self.sort()
        if is_normalized:
            self.normalize()

    def sort(self):
        """
        Sorts the list of notes by midi-note number.
        """
        self.notes.sort(key=lambda x: x.toMidi())

    def normalize(self):
        """
        Brings all notes into one octave (the octave of the tonic is taken as the main one).
        """
        for i, note in enumerate(self.notes):
            self.notes[i].octave = self.tonic.octave

    def __getitem__(self, item):
        return self.notes[item]

    def __str__(self):
        return str({"tonic": self.tonic, "notes": str(self.notes)})

    __repr__ = __str__

    def __len__(self):
        return len(self.notes)


class Piano:
    """
    The piano.
    """

    @staticmethod
    def play_chord(chord, duration=1, delay=0, start_end=True, velocity=64, order=None) -> List[Note]:
        """
        Plays one chord.
        If one value is passed instead of some note parameter,
        then this attribute is set equal to this value for all notes.

        @param chord: Chord, specified as a PianoChord, or list of BasicNote.
        @param duration: Duration in musical note duration.
        @param delay: Delay in musical note duration.
        @param velocity: Volume of note.
        @param order: In what order to play the notes. If None, then play all the notes in the chord in order.
        @param start_end: Delay after the start or end of the previous note.
        @return: List of note.
        """
        _len = len(chord)

        if not hasattr(duration, "__getitem__"):
            duration = [duration] * _len

        if not hasattr(delay, "__getitem__"):
            delay = [delay] * _len

        if not hasattr(start_end, "__getitem__"):
            start_end = [start_end] * _len

        if not hasattr(velocity, "__getitem__"):
            velocity = [velocity] * _len

        if order is None:
            order = [i for i in range(_len)]

        notes = []
        for i, note in enumerate(order):
            notes.append(Note(note=chord[note].note, octave=chord[note].octave, duration=duration[i],
                              velocity=velocity[i], delay=delay[i], start_end=start_end[i]))
        return notes
