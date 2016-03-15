import tempfile
import youtube_dl
import sys
import subprocess
import os
import json
import errno
import numpy
import math

import scipy.io.wavfile as wavfile
import scipy.signal as signal
import scipy.ndimage as ndimage

import matplotlib.pyplot as plt

SAMPLE_FREQ = 11025

def __main__():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    check_ffmpeg_installed()

    check_args()
    global video_id
    video_id = sys.argv[1]

    processed_base_dir = os.path.abspath('../processed-videos/{0}'.format(video_id))
    make_sure_path_exists(processed_base_dir)

    downloaded_audio_file = '{0}/audio'.format(processed_base_dir)
    converted_audio_file = '{0}/audio.wav'.format(processed_base_dir)
    spectrogram_file = '{0}/spectrogram.json'.format(processed_base_dir)

    download_audio(video_id, downloaded_audio_file)
    convert_audio_to_wav(downloaded_audio_file, converted_audio_file)
    write_spectrogram(converted_audio_file, spectrogram_file)

def check_args():
    if len(sys.argv) < 2:
        print("Usage: `python3 process-video.py <youtube video id>`")
        exit(1)

def check_ffmpeg_installed():
    if not os.path.isfile("./ffmpeg"):
        print("Error: `ffmpeg` needs to be installed in {0}".format(os.getcwd()))
        exit(1)

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def log(str=''):
    if str == '':
        print()
    else:
        print('{0}: {1}'.format(video_id, str))
    sys.stdout.flush()

def download_audio(video_id, downloaded_audio_file):
    log()
    log('Downloading audio from video ({0})...'.format(downloaded_audio_file))
    ydl = youtube_dl.YoutubeDL({
        'format': 'worstaudio',
        'outtmpl': downloaded_audio_file,
        'quiet': True,
        'writeinfojson': True
    })
    ydl.download(["https://www.youtube.com/watch?v={0}".format(video_id)])
    log('DONE.')

def convert_audio_to_wav(downloaded_audio_file, converted_audio_file):
    log()
    log('Converting to WAV ({0})...'.format(converted_audio_file))
    subprocess.check_call(["./ffmpeg", "-y", "-i", downloaded_audio_file, "-ar", \
                           str(SAMPLE_FREQ), "-ac", "1", converted_audio_file])
    log('DONE.')

def write_spectrogram(converted_audio_file, spectrogram_file):
    log('')
    log('Writing spectogram ({0})...'.format(spectrogram_file))
    rate, data = wavfile.read(converted_audio_file)
    f, t, Sxx = signal.spectrogram(data, fs=SAMPLE_FREQ, nperseg=1024)

    LSxx = spectrogram_log_frequency_scale(f, Sxx)
    log('Dimensions: {0}'.format(LSxx.shape))

#   Uncomment these lines to plot the logarithmic spectrogram
#    plt.pcolormesh(LSxx)
#    plt.show()

    with open(spectrogram_file, 'w') as f:
        f.write(NumpyAwareJSONEncoder().encode(LSxx))

    log('DONE.')

def spectrogram_log_frequency_scale(freqs, Sxx):
    freqs_logspace = numpy.logspace(0, math.log10(len(freqs)), num=256)
    num_samples = Sxx.shape[1]
    time_linspace = numpy.linspace(0, num_samples-1, num=num_samples)
    LSxx = ndimage.interpolation.map_coordinates(\
                Sxx, \
                numpy.meshgrid(freqs_logspace, time_linspace, indexing='ij'))

    return LSxx

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            if obj.ndim == 1:
                return obj.tolist()
            else:
                return [self.default(obj[i]) for i in range(obj.shape[0])]
            return json.JSONEncoder.default(self, obj)

__main__()
