"""
Contains a description of what a note is.
"""
import copy

NOTES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6,
         "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


class BasicNote:
    """
    Information about note out of time.
    """

    def __init__(self, note: int | str, octave: int):
        """
        :param note: Note (0..11).
        :param octave: Octave.
        """
        if isinstance(note, str):
            self.note = NOTES[note]
        if isinstance(note, int):
            self.note = note
        self.octave = octave
        self._normalize()

    def toMidi(self):
        """
        Converts note and octave number to midi-note number.

        :return: Midi-note number corresponding to the given note and octave.
        """
        return (self.octave + 1) * 12 + self.note

    def _normalize(self):
        """
        Normalize note.

        >>> BasicNote(12, 0) == BasicNote(0, 1)
        True
        """
        n = self.note // 12
        self.note -= 12 * n
        self.octave += n

    def __add__(self, other: int):
        """
        >>> BasicNote(11, 0) + 1 == BasicNote(0, 1)
        True
        Note: Uses 'copy.copy' for copy obejct if class does not consist 'copy' function.
        """
        note = self.copy() if hasattr(self, "copy") else copy.copy(self)
        note.note += other
        note._normalize()
        return note

    def __sub__(self, other: int):
        return self.__add__(-other)

    def __eq__(self, other):
        if isinstance(other, BasicNote):
            return self.note == other.note and self.octave == other.octave
        return False

    def __str__(self):
        return str({"note": self.note, "octave": self.octave})

    __repr__ = __str__


class Note(BasicNote):
    """
    Information about note and her time.
    """

    def __init__(self, note: int, octave: int, velocity: int, duration: float, delay: float, start_end: bool):
        """
        :param note: Note (0..11).
        :param octave: Octave.
        :param duration: Duration in musical note duration.
        :param velocity: Volume of note.
        :param delay: Delay in musical note duration.
        :param start_end: Delay after the start or end of the previous note.
        """
        super().__init__(note, octave)
        self.velocity = velocity
        self.duration = duration
        self.delay = delay
        self.start_end = start_end

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.note == other.note and self.octave == other.octave and \
                   self.velocity == other.velocity and self.duration == other.duration \
                   and self.delay == other.delay and self.start_end == other.start_end
        return False

    def __str__(self):
        return str({"note": self.note, "octave": self.octave, "velocity": self.velocity,
                    "duration": self.duration, "delay": self.delay, "start_end": self.start_end})

    __repr__ = __str__
