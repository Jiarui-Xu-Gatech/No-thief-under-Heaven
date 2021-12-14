from math import pi
from numpy.core.shape_base import block
import pyaudio
import sys
import numpy as np
import aubio
import time
from trans_midi import midi_arr, get_gt
from score_function import generate_score, percentage, forward_or_back
from midi_and_metronome import metronome, play_note
from sklearn.metrics import mean_squared_error
from condition import policeman_step
import pretty_midi
from scipy.io.wavfile import write


class lino_settings():
    def __init__(self):
        self.buffer_size = 2048
        self.pyaudio_format = pyaudio.paFloat32
        self.n_channels = 1
        self.samplerate = 44100
        self.tolerance = 0.8
        self.win_s = self.buffer_size * 4 
        self.hop_s = self.buffer_size
        self.pitch_o = aubio.pitch("default", self.win_s, self.hop_s, self.samplerate)
        


    def midi_arr(self, midi_path):
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        #tempo = midi_data.estimate_tempo()
        tempo = midi_data.get_tempo_changes()[1][0]
        notesClass = midi_data.instruments[0].notes
        pitch_arr = np.zeros((len(notesClass),4))
        for i in range(len(notesClass)):
            tolerance = (notesClass[i].end - notesClass[i].start) / 2 + notesClass[i].end
            pitch_arr[i,:] = np.array([notesClass[i].start, notesClass[i].end, tolerance ,notesClass[i].pitch])
        total_step  = round(len(notesClass) * 0.2, 0)
        self.generateMetronome(midi_path)
        gt_arr = self.check_arr(pitch_arr)
        return gt_arr, tempo, total_step

    def check_arr(self, gt_arr):
        for i in range(gt_arr.shape[0]-1):
            if gt_arr[i,2] > gt_arr [i+1, 0]:
                gt_arr[i, 2] = gt_arr[i+1 , 0]
        return gt_arr

    def generateMetronome(self,filename):
        f_low = self.ToolFreq2Midi(400)
        f_high =self.ToolFreq2Midi(800)
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

    def ToolFreq2Midi(self,fInHz, fA4InHz=440):

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



    
        # self.pitch_o = self.pitch_o.set_unit("midi")
        # self.pitch_o = self.pitch_o.set_tolerance(self.tolerance)

        # self.pitch_o = aubio.pitch("default", self.win_s, self.hop_s, self.samplerate)
        # pitch_o.set_unit("midi")
        # pitch_o.set_tolerance(tolerance)

    def get_pitch(self, audiobuffer):
        signal = np.fromstring(audiobuffer, dtype=np.float32)
        pitch = self.pitch_o(signal)[0]
        return pitch

    def score_strategy(self,gt_cur, pitch, t_cur, gt_arr):
        if (gt_cur == -1 and pitch == 0) or gt_cur == -2 or t_cur <= gt_arr or pitch >= 96:
            return True