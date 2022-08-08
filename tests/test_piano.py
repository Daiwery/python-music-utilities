from unittest import TestCase

from note import NOTES, BasicNote, Note
from piano import PianoChord, Piano


class TestPianoChord(TestCase):
    def test_init(self):
        for note in NOTES.keys():
            _note = BasicNote(0, 3) + NOTES[note]
            assert PianoChord(note, 3, is_normalized=False).notes == [_note, _note + 4, _note + 7], \
                (_note, PianoChord(note, 3))
            assert PianoChord(note + "m", 3, is_normalized=False).notes == [_note, _note + 3, _note + 7], \
                (_note, PianoChord(note + "m", 3))


class TestPiano(TestCase):
    def test_play_chord(self):
        note1 = Note(0, 3, velocity=64, duration=1, delay=0, start_end=True)
        assert Piano.play_chord([BasicNote(0, 3), BasicNote(1, 3)]) == [note1, note1 + 1]

        note2 = Note(1, 3, velocity=100, duration=1 / 2, delay=1 / 8, start_end=False)
        assert Piano.play_chord([BasicNote(0, 3), BasicNote(1, 3)], velocity=[64, 100], duration=[1, 1 / 2],
                                delay=[0, 1 / 8], start_end=[True, False]) == [note1, note2]
