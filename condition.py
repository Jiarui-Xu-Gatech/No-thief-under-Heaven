from math import pi
from os import get_terminal_size
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

def generate_score_tmp(pitch_arr, gt):
    score_tmp = []
    for pitch in pitch_arr:
        score_cur = generate_score(pitch, gt)
        score_tmp.append(score_cur)

    return score_tmp

def policeman_step(pitch_arr, gt, step_cur):
    if gt == 0:
        step = forward_or_back(step_cur, 0)
        return step
    pitch_arr = np.array(pitch_arr)
    score_tmp = generate_score_tmp(pitch_arr, gt)
    percent = percentage(score_tmp)
    step = forward_or_back(step_cur, percent)
    
    return step
    
