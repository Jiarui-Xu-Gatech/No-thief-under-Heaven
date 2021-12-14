#! /usr/bin/env python

# Use pyaudio to open the microphone and run aubio.pitch on the stream of
# incoming samples. If a filename is given as the first argument, it will
# record 5 seconds of audio to this location. Otherwise, the script will
# run until Ctrl+C is pressed.

# Examples:
#    $ ./python/demos/demo_pyaudio.py
#    $ ./python/demos/demo_pyaudio.py /tmp/recording.wav

import pyaudio
import sys
import numpy as np
import aubio
import time

'''
pitch_dic = {
    'C0':0, 'C0#':1, 'D0':2,'D0#':3,'E0':4,'E0#':5,'F0':6,'G0':7,'G0#':8,'A0':9,'A0#':10,'B0':11,
    'C1':12, 'C1#':13, 'D1':14,'D1#':15,'E1':16,'E1#':17,'F1':18,'G1':19,'G1#':20,'A1':21,'A1#':22,'B1':23,
    'C2':24, 'C2#':25, 'D2':26,'D2#':27,'E2':28,'E2#':29,'F2':30,'G2':31,'G2#':32,'A2':33,'A2#':34,'B2':35,
    'C3':36, 'C3#':37, 'D3':38,'D3#':39,'E3':40,'E3#':41,'F3':42,'G3':43,'G3#':44,'A3':45,'A3#':46,'B3':47,
    'C4':48, 'C4#':49, 'D4':50,'D4#':51,'E4':52,'E4#':53,'F4':54,'G4':55,'G4#':56,'A4':57,'A4#':58,'B4':59,
    'C5':60, 'C5#':61, 'D5':62,'D5#':63,'E5':64,'E5#':65,'F5':66,'G5':67,'G5#':68,'A5':69,'A5#':70,'B5':71,
    'C6':72, 'C6#':73, 'D6':74,'D6#':75,'E6':76,'E6#':77,'F6':78,'G6':79,'G6#':80,'A6':81,'A6#':82,'B6':83,
    'C7':84, 'C7#':85, 'D7':86,'D7#':87,'E7':88,'E7#':89,'F7':90,'G7':91,'G7#':92,'A7':93,'A7#':94,'B7':95,
    'C8':96, 'C8#':97, 'D8':98,'D8#':99,'E8':100,'E8#':101,'F8':102,'G8':103,'G8#':104,'A8':105,'A8#':106,'B8':107,
    'C9':108, 'C9#':109, 'D9':110,'D9#':111,'E9':112,'E9#':113,'F9':114,'G9':115,'G9#':116,'A9':117,'A9#':118,'B9':119,
    'C10':120, 'C10#':121, 'D10':122,'D10#':123,'E10':124,'E10#':125,'F10':126,'G10':127    

}

# initialise pyaudio
p = pyaudio.PyAudio()
pitch_arr = np.array(list(pitch_dic))

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

# if len(sys.argv) > 1:
#     # record 5 seconds
#     output_filename = sys.argv[1]
#     record_duration = 5 # exit 1
#     outputsink = aubio.sink(sys.argv[1], samplerate)
#     total_frames = 0
# else:
#     # run forever
#     outputsink = None
#     record_duration = None

# setup pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

print("*** starting recording")
while True:
    try:
        audiobuffer = stream.read(buffer_size)
        signal = np.fromstring(audiobuffer, dtype=np.float32)

        pitch = pitch_o(signal)[0]
        confidence = pitch_o.get_confidence()

        # print("{} / {}".format(pitch,confidence))
        pitch_index = int(round(pitch, 0))
        print("{} / {}".format(pitch,pitch_arr[pitch_index]))
        # time.sleep(0.1)
        # if outputsink:
        #     outputsink(signal, len(signal))

        # if record_duration:
        #     total_frames += len(signal)
        #     if record_duration * samplerate < total_frames:
        #         break
    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break

print("*** done recording")
stream.stop_stream()
stream.close()
p.terminate()
'''
def recordingTool():
    pitch_dic = {
        'C0': 0, 'C0#': 1, 'D0': 2, 'D0#': 3, 'E0': 4, 'E0#': 5, 'F0': 6, 'G0': 7, 'G0#': 8, 'A0': 9, 'A0#': 10,
        'B0': 11,
        'C1': 12, 'C1#': 13, 'D1': 14, 'D1#': 15, 'E1': 16, 'E1#': 17, 'F1': 18, 'G1': 19, 'G1#': 20, 'A1': 21,
        'A1#': 22, 'B1': 23,
        'C2': 24, 'C2#': 25, 'D2': 26, 'D2#': 27, 'E2': 28, 'E2#': 29, 'F2': 30, 'G2': 31, 'G2#': 32, 'A2': 33,
        'A2#': 34, 'B2': 35,
        'C3': 36, 'C3#': 37, 'D3': 38, 'D3#': 39, 'E3': 40, 'E3#': 41, 'F3': 42, 'G3': 43, 'G3#': 44, 'A3': 45,
        'A3#': 46, 'B3': 47,
        'C4': 48, 'C4#': 49, 'D4': 50, 'D4#': 51, 'E4': 52, 'E4#': 53, 'F4': 54, 'G4': 55, 'G4#': 56, 'A4': 57,
        'A4#': 58, 'B4': 59,
        'C5': 60, 'C5#': 61, 'D5': 62, 'D5#': 63, 'E5': 64, 'E5#': 65, 'F5': 66, 'G5': 67, 'G5#': 68, 'A5': 69,
        'A5#': 70, 'B5': 71,
        'C6': 72, 'C6#': 73, 'D6': 74, 'D6#': 75, 'E6': 76, 'E6#': 77, 'F6': 78, 'G6': 79, 'G6#': 80, 'A6': 81,
        'A6#': 82, 'B6': 83,
        'C7': 84, 'C7#': 85, 'D7': 86, 'D7#': 87, 'E7': 88, 'E7#': 89, 'F7': 90, 'G7': 91, 'G7#': 92, 'A7': 93,
        'A7#': 94, 'B7': 95,
        'C8': 96, 'C8#': 97, 'D8': 98, 'D8#': 99, 'E8': 100, 'E8#': 101, 'F8': 102, 'G8': 103, 'G8#': 104, 'A8': 105,
        'A8#': 106, 'B8': 107,
        'C9': 108, 'C9#': 109, 'D9': 110, 'D9#': 111, 'E9': 112, 'E9#': 113, 'F9': 114, 'G9': 115, 'G9#': 116,
        'A9': 117, 'A9#': 118, 'B9': 119,
        'C10': 120, 'C10#': 121, 'D10': 122, 'D10#': 123, 'E10': 124, 'E10#': 125, 'F10': 126, 'G10': 127

    }

    # initialise pyaudio
    p = pyaudio.PyAudio()
    pitch_arr = np.array(list(pitch_dic))

    # open stream
    buffer_size = 1024
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1
    samplerate = 44100
    stream = p.open(format=pyaudio_format,
                    channels=n_channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=buffer_size)
    tolerance = 0.8
    win_s = 4096  # fft size
    hop_s = buffer_size  # hop size
    pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)
    audiobuffer = stream.read(buffer_size)
    signal = np.fromstring(audiobuffer, dtype=np.float32)

    pitch = pitch_o(signal)[0]
    confidence = pitch_o.get_confidence()

    # print("{} / {}".format(pitch,confidence))
    pitch_index = int(round(pitch, 0))
    return pitch
    print("{} / {}".format(pitch,pitch_arr[pitch_index]))
    #except KeyboardInterrupt:
    #stream.stop_stream()
    #stream.close()
    #p.terminate()
    #print("*** Ctrl+C pressed, exiting")
