'''
This is a python file for generating single notes and metronome sound
Reference Article: https://ritza.co/articles/note-generator-article/
'''

import simpleaudio
import numpy
import time

# Note frequencies
notes = {
    1: ["A" ,0],
    2: ["A#",0],
    3: ["B" ,0],
    4: ["C" ,0],
    5: ["C#",0],
    6: ["D" ,0],
    7: ["D#",0],
    8: ["E" ,0],
    9: ["F" ,0],
    10:["F#",0],
    11:["G" ,0],
    12:["G#",0],
}

# Generate note frequencies
for i,note in enumerate(notes.keys()):
    notes[note] = round(440 * 2 ** (i / 12), 1)
    #print(notes[note])
#print(notes)

def play_note(note, octave=4):
    if octave >= 8:
        octave = 8
    frequency = 440*2**((note -69)/12)
    fs = 44100  # 44100 samples per second
    seconds = 1 # Note duration - integer

    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = numpy.linspace(0, seconds, seconds * fs, False)

    # Generate a sine wave from the frequency
    note = numpy.sin(frequency * t * 2 * numpy.pi)

    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / numpy.max(numpy.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(numpy.int16)

    # Start playback
    play_obj = simpleaudio.play_buffer(audio, 1, 2, fs)

# Remove this after testing is done
#play_note(notes[2], octave = 4)
#time.sleep(1)

# Create a metronome, the argument is bpm and mode, mode is the numerator of the time signature.
# For example, 4/4 has a mode of 4, 3/4 has a mode of 3, and 6/8 has a mode of 6
def metronome(bpm, mode):
    #print(float(bpm), "bpm")
    delay = 60/bpm
    count = 0
    beat = 0

    multiple = 8
    t=0
    while t<4:
        wait(delay)

        # increment count after every wait and beat after ever 4 counts
        count += 1
        if count > mode:
            count = 1
            beat += 1

        # set metronome audio according to beat count
        wave_obj = simpleaudio.WaveObject.from_wave_file('metronome.wav')
        if count == 1:
            wave_obj = simpleaudio.WaveObject.from_wave_file('metronomeup.wav')

        # play metronome audio
        play_obj = wave_obj.play()
        play_obj

        t=t+1
        # Remove this after testing
        #print(beat, count)

def wait(delay):
    end_time = time.time() + delay
    while end_time > time.time():
        continue

#Remove this after testing
#metronome(200,6)
