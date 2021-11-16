import pyaudio
import queue
import sys

class Listener:
    def __init__(self,chunk=8192, max_mem_mb = 100, input_id=0, format=pyaudio.paInt16, channels = 2, rate = 44100):
        self.CHUNK = chunk
        self.FORMAT = format
        self.CHANNELS = channels
        self.RATE = rate
        self.INPUT_ID = input_id

        self.p = pyaudio.PyAudio()
        self.frames = Queue.queue()
        self.do_record = 0
        self.sleep_time = 0



    def worker(input_device, out_q):
        stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                input_device_index = self.INPUT_ID
               )
        while(True):
            while(self.do_record):

                for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                self.frames.put(data)

                #memory management
                mem_usage = sys.getsizeof(frames)
                if self.sleep_time>0:
                    time.sleep(self.sleep_time)
                
            while(not self.do_record):
                time.sleep(0.2)


        stream.stop_stream()
        stream.close()
        p.terminate()




    def init_record()
