from unittest import TestCase

from note import NOTES, BasicNote, Note
from piano import PianoChord, Piano


class TestPianoChord(TestCase):
    def test_init(self):
        for name in NOTES.keys():
            note = BasicNote(0, 3) + NOTES[name]
            assert PianoChord(name, 3, is_normalized=False).notes == [note, note + 4, note + 7]
            assert PianoChord(name + "m", 3, is_normalized=False).notes == [note, note + 3, note + 7]


class TestPiano(TestCase):
    def test_play_chord(self):
        note1 = Note(0, 3, velocity=64, duration=1, delay=0, start_end=True)
        assert Piano.play_chord([BasicNote(0, 3), BasicNote(1, 3)]) == [note1, note1 + 1]

        note2 = Note(1, 3, velocity=100, duration=2, delay=8, start_end=False)
        assert Piano.play_chord([BasicNote(0, 3), BasicNote(1, 3)], velocity=[64, 100], duration=[1, 2],
                                delay=[0, 8], start_end=[True, False]) == [note1, note2]

        assert Piano.play_chord([BasicNote(0, 3), BasicNote(1, 3)], velocity=2*[64, 100], duration=2*[1, 2],
                                delay=2*[0, 8], start_end=2*[True, False], order=2*[0, 1]) == 2*[note1, note2]
