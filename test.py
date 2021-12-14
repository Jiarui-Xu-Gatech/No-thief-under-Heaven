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
from lino_settings import lino_settings

inputFile = input("Please input your file name:")
# PATH_TO_MIDI = '/home/lino/Desktop/group 6/test_CSD/midi/en0{}a.mid'.format(inputFile)
PATH_TO_MIDI = '/home/lino/Desktop/group 6/test_POP909/{}.mid'.format(inputFile)


# initialise pyaudio
p = pyaudio.PyAudio()
lino = lino_settings()
# open stream
stream = p.open(format=lino.pyaudio_format,
                channels=lino.n_channels,
                rate=lino.samplerate,
                input=True,
                frames_per_buffer=lino.buffer_size)

# setup pitch
lino.pitch_o.set_unit("midi")
lino.pitch_o.set_tolerance(lino.tolerance)
gt_arr, tempo, total_step = lino.midi_arr(PATH_TO_MIDI)
index = 0
loop_time = 0
step = 0
pitch_list = []


while True:
    # trigger metro and initialize time before game
    if loop_time == 0:
        play_note(gt_arr[0,3], 1)
        metronome(tempo, 4)
        t_start = time.time()

    # get real-time pitch
    audiobuffer = stream.read(lino.buffer_size)
    pitch = lino.get_pitch(audiobuffer)
    
    
    # get current time, gt 
    t_cur = time.time() - t_start
    gt_cur = get_gt(t_cur, gt_arr[index,:])

    if lino.score_strategy(gt_cur, pitch, t_cur, gt_arr[0,0]) == True :
        score = 'null'
    else:
        score = generate_score(pitch, gt_cur)
        pitch_list.append(pitch)
        
    
    # print(t_cur)
    print("pitch_est = {}, pitch_ref = {}, score = {}".format(pitch, gt_cur, score))
    # print('time:', t_cur)
    

    loop_time += 1
    # change to next gt if current time exceed the previous pitch duration
    if t_cur > gt_arr[index, 1] and index != gt_arr.shape[0]-1:
        step = policeman_step(pitch_list, gt_arr[index, 3], step)
        index += 1
        pitch_list=[]
        print("----------------------------------------To win, you need:", total_step - step, " more steps!------------------------------------------")
        if total_step == step:
            print('----------------------------------------You Win!!!------------------------------------------')
            print('Total steps to win:{}, you spend:{} '.format(total_step, index))
            break
        score_tmp = []

    # game over if there is no gt
    if index == gt_arr.shape[0]-1 and t_cur > gt_arr[index, 1]:
        percent = percentage(score_tmp)
        score_tmp = []
        break
    


       
# stream.stop_stream()
# stream.close()
# p.terminate()