from unittest import TestCase

from composition import Sequence
from midiUtilities import MidiMessage
from note import Note


class TestSequence(TestCase):
    def test_toMidi(self):
        n1 = Note(0, 0, velocity=64, duration=1, delay=0, start_end=True)
        n2 = Note(1, 0, velocity=64, duration=1, delay=1, start_end=False)
        n3 = Note(2, 0, velocity=64, duration=1, delay=1, start_end=True)
        s = Sequence([n1, n2, n3], "1")

        result = s.toMidi()
        assert result[1] == 4
        assert result[0] == [MidiMessage("note_on", 0, note=0, velocity=64),
                             MidiMessage("note_off", 1, note=0, velocity=64),
                             MidiMessage("note_on", 2, note=1, velocity=64),
                             MidiMessage("note_off", 3, note=1, velocity=64),
                             MidiMessage("note_on", 3, note=2, velocity=64),
                             MidiMessage("note_off", 4, note=2, velocity=64)]

    def test_compile_with_many_tracks(self):
        n1 = Note(0, 0, velocity=64, duration=1, delay=0, start_end=True)
        n2 = Note(1, 0, velocity=64, duration=1, delay=1, start_end=False)
        n3 = Note(2, 0, velocity=64, duration=1, delay=1, start_end=True)

        s1 = Sequence([n1, n2, n3], "1")
        s2 = Sequence([n1, n2, n3], "2")
        s3 = Sequence([n1, n2, n3], "1")
        s1.next_sequences += [s2, s3]

        result = s1.compile()
        assert result[0] == ("1", [MidiMessage("note_on", 0, note=0, velocity=64),
                                   MidiMessage("note_off", 1, note=0, velocity=64),
                                   MidiMessage("note_on", 2, note=1, velocity=64),
                                   MidiMessage("note_off", 3, note=1, velocity=64),
                                   MidiMessage("note_on", 3, note=2, velocity=64),
                                   MidiMessage("note_off", 4, note=2, velocity=64)])
        assert result[1] == ("2", [MidiMessage("note_on", 4, note=0, velocity=64),
                                   MidiMessage("note_off", 5, note=0, velocity=64),
                                   MidiMessage("note_on", 6, note=1, velocity=64),
                                   MidiMessage("note_off", 7, note=1, velocity=64),
                                   MidiMessage("note_on", 7, note=2, velocity=64),
                                   MidiMessage("note_off", 8, note=2, velocity=64)])
        assert result[2] == ("1", [MidiMessage("note_on", 4, note=0, velocity=64),
                                   MidiMessage("note_off", 5, note=0, velocity=64),
                                   MidiMessage("note_on", 6, note=1, velocity=64),
                                   MidiMessage("note_off", 7, note=1, velocity=64),
                                   MidiMessage("note_on", 7, note=2, velocity=64),
                                   MidiMessage("note_off", 8, note=2, velocity=64)])
