import pyaudio
from threading import Thread
import curses
import sys
import numpy
import scipy
import scipy.signal as signal
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import math
import uuid
import json
import os
import errno
import wave
from keras.models import model_from_json

quit = False
test = False
dump_0 = False
dump_1 = False
dump_complete = False

audio = pyaudio.PyAudio()

RATE = 22050
CHUNK = 1024
BUFFER_SECS = 1.03
FORMAT=pyaudio.paInt16

model = None
model = model_from_json(open('my_model_architecture.json').read())
model.load_weights('my_model_weights.h5')

def getchar():
    import tty, sys, termios  # raises ImportError if unsupported

    fd = sys.stdin.fileno()
    oldSettings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        answer = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

    return answer

class AudioRecording(Thread):
    def run(self):
        stream = audio.open(format=FORMAT,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []
        test_frames = []

        global quit
        global dump_0
        global dump_1
        global dump_complete
        global test

        num_frames = 0

        while not quit:
            num_frames = num_frames + 1
            if num_frames > 23 and ((num_frames % 15) == 0) and model:
                test = True

            data = stream.read(CHUNK)
            test_frames.append(data)
            if len(test_frames) > BUFFER_SECS * RATE / CHUNK:
                test_frames.pop(0)

            if dump_0 or dump_1:
                frames.append(data)

                if dump_complete:
                    DumpFrames(frames, 1 if dump_1 else 0).start()
                    dump_complete = False
                    dump_0 = False
                    dump_1 = False
                    frames = []

            if test:
                TestFrames(test_frames).start()
                test = False

        stream.stop_stream()
        stream.close()
        audio.terminate()

class DumpFrames(Thread):
    def __init__(self, frames, audio_class):
        Thread.__init__(self)
        self.frames = frames
        self.audio_class = audio_class

    def run(self):
        snippet_id = uuid.uuid4()
        dir = 'data/{0}/{1}'.format(self.audio_class, snippet_id)
        make_sure_path_exists(dir)
        waveform = b''.join(self.frames)
        save_mp3_file(dir, waveform)
        print "Saved in {0}\r\n".format(dir)

class TestFrames(Thread):
    def __init__(self, frames):
        Thread.__init__(self)
        self.frames = frames

    def run(self):
        waveform = b''.join(self.frames)
        f, t, Sxx = signal.spectrogram(map(ord, waveform), fs=RATE)
        LSxx = spectrogram_log_frequency_scale(f, Sxx)

        # Convert from 128x201 to 128x196 as the model expects
        LSxx = numpy.delete(LSxx, [0,1,2,3,4], axis=1)

        LSxx = numpy.expand_dims(LSxx, axis=0) # Make into tensor with depth 1, as that's the input to a ConvNet
        LSxx = numpy.expand_dims(LSxx, axis=0) # Make into data set with size 1
        prediction = model.predict(LSxx)[0][0]
        print prediction
        print '\r\n'
        if prediction > 0.99:
            PlayStopWhistling().start()

class PlayStopWhistling(Thread):
    def run(self):
        # open the file for reading.
        wf = wave.open('stop-whistling.wav', 'rb')

        # open stream based on the wave object which has been input.
        stream = audio.open(format = audio.get_format_from_width(wf.getsampwidth()),
                            channels = wf.getnchannels(),
                            rate = wf.getframerate(),
                            output = True)

        # read data (based on the chunk size)
        data = wf.readframes(CHUNK)

        # play stream (looping from beginning of file to the end)
        while data != '':
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(CHUNK)

        # cleanup stuff.
        stream.close()

def save_mp3_file(dir, waveform):
    waveFilename = '{0}/audio.wav'.format(dir)
    waveFile = wave.open(waveFilename, 'wb')
    waveFile.setnchannels(1)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(waveform)
    waveFile.close()

    mp3Filename = '{0}/audio.mp3'.format(dir)
    os.system('ffmpeg -i {0} -vn -ar {1} -ac 1 -ab 128k -f mp3 {2}'.format(
        waveFilename, RATE, mp3Filename))

def save_spectrogram(dir, waveform):
    f, t, Sxx = signal.spectrogram(map(ord, waveform), fs=RATE)
    LSxx = spectrogram_log_frequency_scale(f, Sxx)
    numpy.save('{0}/spectrogram.npy'.format(dir), LSxx)
    scipy.misc.imsave('{0}/spectrogram.png'.format(dir), LSxx)

def save_class(dir, is_class_1):
    with open('{0}/class'.format(dir), 'w') as file:
        file.write('1\n' if is_class_1 else '0\n')

def spectrogram_log_frequency_scale(freqs, Sxx):
    freqs_logspace = numpy.logspace(0, math.log10(len(freqs)), num=128)
    num_samples = Sxx.shape[1]
    time_linspace = numpy.linspace(0, num_samples-1, num=num_samples)
    LSxx = ndimage.interpolation.map_coordinates(
        Sxx,
        numpy.meshgrid(freqs_logspace, time_linspace, indexing='ij'))

    return LSxx

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def main():
    AudioRecording().start()

    global quit
    global dump_1
    global dump_0
    global dump_complete
    global test

    while not quit:
        ch = getchar()
        if ch == 'q':
            quit = True
        elif ch == 't':
            test = True
        elif ch == '1':
            dump_1 = True
        elif ch == '0':
            dump_0 = True
        elif ch == '-':
            dump_complete = True

os.chdir(os.path.dirname(os.path.abspath(__file__)))
main()
