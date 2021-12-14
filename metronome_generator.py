import pretty_midi
import numpy as np
from scipy.io.wavfile import write

# Helper Functions
def ToolFreq2Midi(fInHz, fA4InHz=440):
    def convert_freq2midi_scalar(f, fA4InHz):

        if f <= 0:
            return 0
        else:
            return (69 + 12 * np.log2(f / fA4InHz))

    fInHz = np.asarray(fInHz)
    if fInHz.ndim == 0:
        return convert_freq2midi_scalar(fInHz, fA4InHz)

    midi = np.zeros(fInHz.shape)
    for k, f in enumerate(fInHz):
        midi[k] = convert_freq2midi_scalar(f, fA4InHz)

    return (midi)

f_low = ToolFreq2Midi(800)
f_high =ToolFreq2Midi(1600)
print("frequency choices")
print(f_low,f_high)

# Load MIDI file into PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('001.mid')
# Load MIDI Tempo, calculate time interval between beats
tempo = midi_data.get_tempo_changes()[1][0]
#timePerBeat = 60/tempo
# Find the first onset time of MIDI
#first_onset = midi_data.get_onsets()[0]
# Get Beat list of timing
beats = midi_data.get_beats()
# print(beats)

# Create a PrettyMIDI object
metronome = pretty_midi.PrettyMIDI(initial_tempo=tempo)
# Create an Instrument instance for a cello instrument
piano = pretty_midi.Instrument(program=0)
for idx, i in enumerate(beats):
    if ((idx+1) % 4) ==1:
        note_number = 91
    else: 
        note_number = 79
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=i, end=i+0.2)
    piano.notes.append(note)
metronome.instruments.append(piano)
metronome.write('metroTest.mid')
syn = metronome.synthesize()
# print(syn[:500])
samplerate = 44100
write("example.wav", samplerate, syn.astype(np.float32))

