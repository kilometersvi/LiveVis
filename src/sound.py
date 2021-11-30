import pyaudio
import time
import queue
from av import audio
import numpy as np
import scipy.io.wavfile as wav
import librosa
import threading
from statistics import stdev, mean
from math import log10
from scipy import signal

#This library helps us in plotting the  audio
import matplotlib.pyplot as plt


def plotAudio2(output):
        fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(20,4))
        plt.plot(output, color='blue')
        ax.set_xlim((0, len(output)))
        plt.show()


class FrameHandler(threading.Thread):
    #record frames from stream and add to queue

    def __init__(self, chunk=2048, rate=44100, input_device=6, plot=False):
        threading.Thread.__init__(self)

        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = rate
        self.CHUNK = chunk
        self.input_device = input_device
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.data_queue = queue.Queue()
        self.plot = plot

        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  input_device_index=self.input_device,
                                  frames_per_buffer=self.CHUNK
                                 )#stream_callback=self.callback,

    def stop(self):
        self.stream.close()
        self.p.terminate()

    '''
    def callback(self, in_data, frame_count, time_info, flag):
        numpy_array = np.frombuffer(in_data, dtype=np.float32)
        librosa.feature.mfcc(numpy_array)
        return None, pyaudio.paContinue
    '''

    def run(self):
        while (self.stream.is_active()): # if using button you can set self.stream to 0 (self.stream = 0), otherwise you can use a stop condition
            data = self.stream.read(self.CHUNK)

            npdata = np.frombuffer(data, dtype=np.float32)

            self.data_queue.put(npdata)

            if self.plot:
                plotAudio2(numpydata)



class SmallSample:

    def __init__(self, frame, bpm, db):
        self.frame = frame
        self.bpm = bpm
        self.peak_db = db

class AudioHandler(threading.Thread):
    #calculate tempo & note onsets every specified interval (seconds)

    def __init__(self, interval=1.0, input_device=6, plot=False, min_db=-45):
        threading.Thread.__init__(self)

        self.interval = interval
        self.RATE = 44100
        self.CHUNK = int((self.RATE * self.interval) // 5)
        print("chunk: {}".format(self.CHUNK))
        self.input_device = input_device

        self.prev_bpm = 120.0
        self.min_db = min_db

        self.data_queue = queue.Queue()

        self.framehandler = FrameHandler(chunk=self.CHUNK, input_device=self.input_device, plot=plot)

        self.framehandler.start()

    def is_active(self):
        return self.framehandler.stream.is_active()

    def run(self):
        while (self.framehandler.stream.is_active()):

            if self.framehandler.data_queue.qsize() >= 5:

                framesL = []
                for i in range(5):
                    framesL.append(self.framehandler.data_queue.get())

                #combine frames into 1 long frame spanning interval
                data_ronly = np.hstack(framesL)

                #copy data as data is read only
                data = np.array(data_ronly).copy()

                tempo = librosa.beat.tempo(y=data, sr=self.RATE, start_bpm=self.prev_bpm)[0]
                prev_bpm = tempo

                rms = np.max(librosa.feature.rms(y=data))
                peak_db = 20 * log10(rms)

                #if silence, reset prev_bpm
                if (peak_db < self.min_db):
                    self.prev_bpm=120

                sample = SmallSample(data, tempo, peak_db)

                #print(tempo)

                self.data_queue.put(sample)


            else:
                #wait until framehandler reads enough
                time.sleep(0.02)


    def stop(self):
        self.framehandler.stop()

#must use pre-initialized np array to efficiently use contiguous memory in nparray
class Listlike:
    def __init__(self, items, dtype):
        self.arr = np.zeros([items,], dtype=dtype)
        self.end = 0

    #return slice up to index & pop elements
    #assumes is not accessed with out of bounds index
    def pop_to(self,index):
        slice = self.arr[:index]
        #dif = self.end-(self.end-index)
        #print(f"sliced up to {index}. setting 0:{self.end} to index {index}:{self.end} plus {dif} zeros")
        #newvals = np.zeros([self.end,])
        #newvals[]
        #print(self.arr[index:self.end].shape[0])
        #print(np.zeros([self.end-(self.end-index),], dtype=np.float32).shape[0])
        hstak = np.concatenate([self.arr[index:self.end], np.zeros([index,], dtype=np.float32)])
        #print(hstak.shape[0])
        self.arr[:self.end] = hstak
        self.end -= index
        return slice

    #extend collection
    def extend(self, oarr):
        self.arr[self.end:self.end+oarr.shape[0]] = oarr[:]
        self.end += oarr.shape[0]
        #print(f"extended by {oarr.shape[0]}. now at length {self.end}")

    #intuitive size accessor
    def size(self):
        return self.end

def gain(arr, descendedMax, gain=0.8):
    arr = (arr / descendedMax) * gain
    return arr

# modified from https://stackoverflow.com/questions/44013269/recorded-audio-of-one-note-produces-multiple-onset-times
def detect_pitch(y, sr, n_fft=512, onset_offset=5, fmin=75, fmax=1400):
  y = highpass_filter(y, sr)

  o_env = librosa.onset.onset_strength(y, sr=sr)
  times = librosa.frames_to_time(np.arange(len(o_env)), sr=sr)

  onset_frames = librosa.onset.onset_detect(y=o_env, sr=sr)
  pitches, magnitudes = librosa.piptrack(y=y, sr=sr, n_fft=n_fft, center=False, fmin=fmin, fmax=fmax)

  notes = []

  for i in range(0, len(onset_frames)):
    onset = onset_frames[i] + onset_offset
    index = magnitudes[:, onset].argmax()
    pitch = pitches[index, onset]
    if (pitch != 0):
      notes.append(librosa.hz_to_note(pitch, octave=False))

  return notes

def highpass_filter(y, sr):
  filter_stop_freq = 70  # Hz
  filter_pass_freq = 100  # Hz
  filter_order = 1001

  # High-pass filter
  nyquist_rate = sr / 2.
  desired = (0, 0, 1, 1)
  bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
  filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

  # Apply high-pass filter
  filtered_audio = signal.filtfilt(filter_coefs, [1], y)
  return filtered_audio


class IntervalSample:
    def __init__(self, bpm, notes=[], onsets=[], frame=[]):
        self.bpm = bpm
        self.notes = notes
        self.onsets = onsets
        self.frame = frame
        #self.onsets = onsets



class IntervalStream(threading.Thread):
    #packages samples into measure intervals (quarter, eighth, etc) based on estimated bpm

    def __init__(self, interval = 0.125, input_device=6, plot=False, min_db=-45):
        threading.Thread.__init__(self)

        self.input_device=input_device
        self.interval = interval
        self.min_db = min_db
        self.plot = plot

        self.bpm = -1
        self.bpmhist = []


        self.data_queue = queue.Queue()

        self.audiohandler = AudioHandler(interval=0.125, input_device=input_device)

        self.audiohandler.start()

    def run(self):
        prior_frames = Listlike(9999999, dtype=np.float32)
        i = 0
        while (self.audiohandler.is_active()):
            if self.audiohandler.data_queue.qsize() > 0:
                sample_curr = self.audiohandler.data_queue.get()

                #if silence, reset memory
                if (sample_curr.peak_db < self.min_db):
                #if (self.bpm == -1) and (np.mean(sample_curr.frame) < 0.0005):
                    #print(np.mean(sample_curr.frame))
                    self.bpm_hist = []
                    self.bpm = -1
                    #print(sample_curr.peak_db)
                    continue




                prior_frames.extend(sample_curr.frame)

                #print(sample_curr.bpm)

                #converge on bpm
                if self.bpm == -1:
                    self.bpm = sample_curr.bpm
                    self.bpmhist.append(sample_curr.bpm)

                elif len(self.bpmhist)==1:
                    self.bpmhist.append(sample_curr.bpm)
                    self.bpm = mean(self.bpmhist)

                else:
                    standev = stdev(self.bpmhist)

                    #catch miscalculations in bpm (twice expected, half expected)
                    if sample_curr.bpm > self.bpm + standev:
                        if (sample_curr.bpm / 2 < self.bpm + standev) and (sample_curr.bpm / 2 > self.bpm - standev):
                            self.bpmhist.append(sample_curr.bpm / 2)
                        else:
                            self.bpmhist.append(sample_curr.bpm)
                    if sample_curr.bpm < self.bpm - standev:
                        if (sample_curr.bpm * 2 < self.bpm + standev) and (sample_curr.bpm * 2 > self.bpm - standev):
                            self.bpmhist.append(sample_curr.bpm * 2)
                        else:
                            self.bpmhist.append(sample_curr.bpm)

                    self.bpm = mean(self.bpmhist)

                    #prevent bpmhist from growing too large
                    if len(self.bpmhist) > 3:
                        self.bpmhist.pop(0)

                '''
                curr_bpm = librosa.beat.tempo(y=prior_frames.arr, sr=self.audiohandler.RATE)[0]

                #converge on bpm
                if self.bpm == -1:
                    self.bpm = curr_bpm
                    self.bpmhist.append(curr_bpm)

                elif len(self.bpmhist)==1:
                    self.bpmhist.append(curr_bpm)
                    self.bpm = mean(self.bpmhist)

                else:
                    standev = stdev(self.bpmhist)

                    #catch miscalculations in bpm (twice expected, half expected)
                    if curr_bpm > self.bpm + standev:
                        if (curr_bpm / 2 < self.bpm + standev) and (curr_bpm / 2 > self.bpm - standev):
                            self.bpmhist.append(curr_bpm / 2)
                        else:
                            self.bpmhist.append(curr_bpm)
                    if curr_bpm < self.bpm - standev:
                        if (curr_bpm * 2 < self.bpm + standev) and (curr_bpm * 2 > self.bpm - standev):
                            self.bpmhist.append(curr_bpm * 2)
                        else:
                            self.bpmhist.append(curr_bpm)

                    self.bpm = mean(self.bpmhist)

                    #prevent bpmhist from growing too large
                    if len(self.bpmhist) > 10:
                        self.bpmhist.pop(0)
                '''


                #calculate frames per interval. 1/( bpm beats/minute )*60seconds/min * 4beats/measure * 44100 frames/second = frames/measure, *= interval = frames/interval
                #assume 4/4
                FramesPerInterval = int(1/(self.bpm/60)*4*self.interval*self.audiohandler.RATE)
                #print(FramesPerInterval)
                if (prior_frames.size() > FramesPerInterval):

                    c_data = prior_frames.pop_to(FramesPerInterval)

                    #notes = detect_pitch(c_data, sr = self.audiohandler.RATE)

                    onsets = librosa.onset.onset_detect(y = c_data, sr = self.audiohandler.RATE, units='samples')
                    #strengths = librosa.onset.onset_strength(y = c_data, sr = self.audiohandler.RATE)
                    #print(strengths.shape[0])
                    #print(c_data.shape[0])

                    self.data_queue.put(IntervalSample(self.bpm, onsets=onsets, frame=c_data))
                    print(f"BPM: {self.bpm}, Onsets: {onsets}")#, Notes: {notes}")
            else:
                time.sleep(0.02)








if __name__ == '__main__':
    p = pyaudio.PyAudio()

    #view mics on system
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    devices = {}
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                devices[i] =  p.get_device_info_by_host_api_device_index(0, i).get('name')
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    device_id = -1
    for k,v in devices.items():
        if "Scarlett" in v:
            device_id = k
    if device_id == -1:
        print("Scarlett not found")
        exit()

    print("Scarlett ID: {}".format(device_id))
    audio = IntervalStream(interval=0.125, input_device=device_id, min_db=-45)
    print("audio initialized")
    audio.start()
    print("audio started")
