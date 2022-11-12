from composition import Composition, Sequence
from midiUtilities import write_to_file
from piano import *
from synth import synth

c = Composition()

c.add_track("p", 0)  # Piano
s = c.add_sequence(Sequence(Piano.play_chord(PianoChord("E"), 1 / 4), "p"))
s += Sequence(Piano.play_chord(PianoChord("E"), 1 / 8, start_end=False), "p")
s += Sequence(Piano.play_chord(PianoChord("D"), 1 / 4), "p")
s += Sequence(Piano.play_chord(PianoChord("D"), 1 / 8, start_end=False), "p")
s += Sequence(Piano.play_chord(PianoChord("Am"), 1 / 4), "p")
s += Sequence(Piano.play_chord(PianoChord("Am"), 1 / 8, start_end=False, order=2 * [0, 1, 2, 1]), "p")
s += Sequence(Piano.play_chord(PianoChord("E"), 1 / 4 + 1 / 8), "p")
s += Sequence(Piano.play_chord(PianoChord("D"), 1 / 4 + 1 / 8), "p")
s += Sequence(Piano.play_chord(PianoChord("Am"), 1 / 4 + 1 / 8), "p")

write_to_file(c.compile(), r"C:\Users\anluk\Desktop", bmp=120)
synth(c.compile(), bmp=120, sound_font=r"C:\Users\anluk\Documents\lmms\samples\soundfonts\FluidR3_GM.sf2")
