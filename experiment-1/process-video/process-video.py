import tempfile
import youtube_dl
import sys
import subprocess
import spectrogram
import os
import json
import errno
import numpy
import scipy.io.wavfile as wavfile
import scipy.signal as signal

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if len(sys.argv) < 2:
    print("Usage: `python3 process-video.py <youtube video id>`")
    exit(1)

if not os.path.isfile("./ffmpeg"):
    print("Error: `ffmpeg` needs to be installed in {0}".format(os.getcwd()))
    exit(1)

videoId = sys.argv[1]
url = "https://www.youtube.com/watch?v=${0}".format(videoId)

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
        print('{0}: {1}'.format(videoId, str))
    sys.stdout.flush()

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            if obj.ndim == 1:
                return obj.tolist()
            else:
                return [self.default(obj[i]) for i in range(obj.shape[0])]
            return json.JSONEncoder.default(self, obj)

processed_base_dir = os.path.abspath('../processed-videos/{0}'.format(videoId))
make_sure_path_exists(processed_base_dir)
downloaded_audio_file = '{0}/audio'.format(processed_base_dir)
converted_audio_file = '{0}/audio.wav'.format(processed_base_dir)
spectrogram_file = '{0}/spectrogram.json'.format(processed_base_dir)

log()
log('Downloading audio from video ({0})...'.format(downloaded_audio_file))
ydl = youtube_dl.YoutubeDL({
    'format': 'worstaudio',
    'outtmpl': downloaded_audio_file,
    'quiet': True
})
ydl.download(["https://www.youtube.com/watch?v={0}".format(videoId)])
log('DONE.')

log()
log('Converting to WAV ({0})...'.format(converted_audio_file))
subprocess.check_call(["./ffmpeg", "-y", "-i", downloaded_audio_file, "-ar", \
                       "11025", "-ac", "1", converted_audio_file])
log('DONE.')

log('')
log('Writing spectogram ({0})...'.format(spectrogram_file))
rate, data = wavfile.read(converted_audio_file)
f, t, Sxx = signal.spectrogram(data, fs=11025)
log('Dimensions: {0}x{1}'.format(f.size, t.size))
with open(spectrogram_file, 'w') as f:
    f.write(NumpyAwareJSONEncoder().encode(Sxx))
log('DONE.')
