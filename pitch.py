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
from playsound import playsound
from threading import Thread

inputFile = input("Please input your file name:")
# PATH_TO_MIDI = '/home/lino/Desktop/group 6/test_CSD/midi/en0{}a.mid'.format(inputFile)
PATH_TO_MIDI = '/home/lino/Desktop/group 6/test_POP909/{}.mid'.format(inputFile)


# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 2048
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)
# setup pitch
tolerance = 0.8
win_s = buffer_size * 4 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

# initialize gt_file, index of gt_file, loop_time and initial score
gt_arr, tempo, total_step = midi_arr(PATH_TO_MIDI)
index = 0
loop_time = 0
print(gt_arr)
# score = 50
# initialize score lists
score_tmp = []
score_arr = np.zeros(gt_arr.shape[0])
step = 0
rms_qy = []
print("{} notes you need sing correctly".format(total_step))

while True:
    # trigger metro and initialize time before game
    if loop_time == 0:
        play_note(gt_arr[0,3], 1)
        
        metronome(tempo, 4)
        
        # playsound('/home/lino/Desktop/group 6/test_POP909/{}.wav'.format(inputFile), block=False)
        # thread = Thread(target= playsound('/home/lino/Desktop/group 6/test_POP909/{}.wav'.format(inputFile)))
        # thread = Thread(target= palyy())
        # thread.start()
        t_start = time.time()

    # get real-time pitch
    audiobuffer = stream.read(buffer_size)
    signal = np.fromstring(audiobuffer, dtype=np.float32)
    pitch = pitch_o(signal)[0]
    
    # get current time, gt and score
    t_cur = time.time() - t_start
    
    gt_cur = get_gt(t_cur, gt_arr[index,:])

    if (gt_cur == -1 and pitch == 0) or gt_cur == 'in_tolerance' or t_cur <= gt_arr[0,0] or pitch >= 96:
        score = 'null'
    else:
        score = generate_score(gt_cur, pitch)
        score_tmp.append(score)
    
    # print(t_cur)
    print("pitch_est = {}, pitch_ref = {}, score = {}".format(pitch, gt_cur, score))
    print('time:', t_cur)
    

    loop_time += 1
    # change to next gt if current time exceed the previous pitch duration
    if t_cur > gt_arr[index, 1] and index != gt_arr.shape[0]-1:
        percent = percentage(score_tmp)
        # score_list
        score_arr[index] = percent # use for whole song
        rms_qy.append(percent) # use for rms
        index += 1
        step = forward_or_back(step, percent)
        print("----------------------------------------To win, you need:", total_step - step, " more steps!------------------------------------------")
        if total_step == step:
            print('----------------------------------------You Win!!!------------------------------------------')
            print('Total steps to win:{}, you spend:{} '.format(total_step, index))

            break
        score_tmp = []

    # game over if there is no gt
    if index == gt_arr.shape[0]-1 and t_cur > gt_arr[index, 1]:
        percent = percentage(score_tmp)
        score_arr[index] = percent
        score_tmp = []
        rms_qy.append(percent)
        break
    


rms_arr = np.array(rms_qy)
test = np.ones(rms_arr.shape[0])
rms = np.sqrt(mean_squared_error(rms_arr / 100, test))
print(rms_arr)
print('Rms:', rms)


# use for whole song
# print('percentage:', score_arr)
# test = np.ones(score_arr.shape[0])
# rms = np.sqrt(mean_squared_error(score_arr / 100, test))
# print('Rms:', rms)

       
    


    
  


# stream.stop_stream()
# stream.close()
# p.terminate()