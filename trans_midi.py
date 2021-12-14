
from numpy.core.defchararray import array
import pyaudio
import sys
import numpy as np
import aubio
import time
import pretty_midi

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


def generateMetronome(filename):
    f_low = ToolFreq2Midi(400)
    f_high =ToolFreq2Midi(800)
    print("frequency choices")
    print(f_low,f_high)

    # Load MIDI file into PrettyMIDI object
    midi_data = pretty_midi.PrettyMIDI(filename)
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
 
    samplerate = 44100
    wav_name = filename[:-4]
    write(wav_name + ".wav", samplerate, syn.astype(np.float32))
  

def midi_arr(midi_path):
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    #tempo = midi_data.estimate_tempo()
    tempo = midi_data.get_tempo_changes()[1][0]
    notesClass = midi_data.instruments[0].notes
    pitch_arr = np.zeros((len(notesClass),4))
    for i in range(len(notesClass)):
        tolerance = (notesClass[i].end - notesClass[i].start) / 2 + notesClass[i].end
        pitch_arr[i,:] = np.array([notesClass[i].start, notesClass[i].end, tolerance ,notesClass[i].pitch])
    total_step  = round(len(notesClass) * 0.2, 0)
    generateMetronome(midi_path)
    gt_arr = check_arr(pitch_arr)
    return gt_arr, tempo, total_step

def check_arr(gt_arr):
    for i in range(gt_arr.shape[0]-1):
        if gt_arr[i,2] > gt_arr [i+1, 0]:
            gt_arr[i, 2] = gt_arr[i+1 , 0]
    return gt_arr

def get_gt(t_cur, gt_arr):
    if t_cur >= gt_arr[0] and t_cur <= gt_arr[1]:
        gt_cur = gt_arr[3]
    elif t_cur <= gt_arr[2] and t_cur >= gt_arr[1]: 
        gt_cur = -2
    else:
        gt_cur = -1
    return gt_cur

# a, b, c = midi_arr('/home/lino/Desktop/group 6/test_POP909/714.mid')