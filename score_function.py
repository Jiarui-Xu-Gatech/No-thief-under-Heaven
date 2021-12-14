import time
from math import log, pow
import numpy as np
import matplotlib.pyplot as plt



def in_one_octave(pitch_ref, pitch_est):
    diff = abs(pitch_ref - pitch_est)
  
    while(diff > 6):
        if pitch_ref >= pitch_est:
            pitch_est += 12
        else:
            pitch_est -= 12
        
        
        diff = abs(pitch_ref - pitch_est)
        

    return pitch_est

def norm(x, x_min, x_max):
    y_min = 0
    y_max = np.pi
    y = y_min + ((y_max - y_min) / (x_max - x_min)) * (x- x_min)
    return y

def scoring(pitch_ref, pitch_est_new):
    pitch_ref_left = pitch_ref - 1
    pitch_ref_right = pitch_ref + 1
    if pitch_est_new <= pitch_ref_left or pitch_est_new >= pitch_ref_right:
        return 0
    else:
        diff = abs(pitch_ref - pitch_est_new)
        if diff <= 0.75:
            tmp = norm(pitch_est_new, pitch_ref, pitch_ref_right)
            score = 50 * np.cos(tmp / 2) +50
        else:
            com = lambda x: -277 * x + 277
            score = com(diff)
    return score

def generate_score(pitch_ref, pitch_est):
    if pitch_est == 0 or pitch_ref == -1:
        return 0
    pitch_est_new = in_one_octave(pitch_ref, pitch_est)
    score = scoring(pitch_ref, pitch_est_new)
    return score
    # return (score - 50) / 10

def percentage(score_list):
    if score_list == []:
        return 0
    tmp = np.array(score_list)
    tmp = np.unique(tmp)
    per_arr = tmp[np.where(tmp >= 30)]
    percentage = per_arr.shape[0] / tmp.shape[0]
    return percentage * 100

def forward_or_back(step,percent):
    if percent >= 80:
        return step + 1
    else:
        if step == 0:
            return step
        else:
            return step - 1 





