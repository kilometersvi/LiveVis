import cv2
import numpy as np
import threading
import queue
import time
import random

from layers.full_color import FullColor
from layers.color_mix_2split import ColorMix2Split
from layers.split4 import Split4
from layers.checker import Checkerboard
from sound import IntervalStream, IntervalSample

class LayerHandler:

    @staticmethod
    def combineLayers(layers, params={}):
        current = []
        for l in layers:
            current = l.compute(current, params)
            l.n_l += 1

        return current

    @staticmethod
    def randomLayers(possibleLayers, weights):
        randNum = random.randint(2, len(possibleLayers)-2)

        #print(f"possibleLayers: {possibleLayers}, randNum: {randNum}")

        choices = random.choices(possibleLayers, weights=weights, k=randNum)

        #print(f"choices: {choices}")

        '''
        while sum(int(isinstance(l, FullColor)) for l in choices) > 1:
            indices = []
            for i in range(len(choices)):
                if isinstance(choices[i], FullColor):
                    indices.append(i)
            choices.pop(indices[-1])
        '''
        new_layers = [FullColor(config={'color':(0,0,0,1.0)})]
        new_layers.extend(choices)

        #print(f"randomLayers: {new_layers}")
        return new_layers


    @staticmethod
    def preprocess(frame,ftoi=True):
        if ftoi:
            frame = (frame * 255).astype('uint8')
        return frame

    @staticmethod
    def Show(frame, ftoi=True, cv2Show=False):
        if ftoi:
            frame = (frame * 255).astype('uint8')
        if cv2Show:
            print(f"frame dtype: {frame.dtype}")

            cv2.imshow( "LiveVis", frame)
        else:
            return frame


class LayerController(threading.Thread):

    def __init__(self,device_id, resolution=16):
        threading.Thread.__init__(self)

        self.n = 0
        self.bpm = -1
        self.frameTime = 0
        self.meter_length = 0

        #show frame ever 1/resolution measures (smaller = faster frames)
        self.resolution = resolution

        self.running = True

        #ColorMix2Split()
        self.possibleLayers = [
            Checkerboard(),
            Checkerboard(config={'numSquares':8, 'thickness':2, 'colorRand':True}),
            Split4(),
            Split4(),
            Split4(),
            ColorMix2Split()
        ]
        self.weights = [
            2,
            1,
            1,
            1,
            1,
            2
        ]
        self.layers = [FullColor(config={'color':(0.5,0.5,0.5,1.0)})]

        self.IntervalStream = IntervalStream(interval=0.125, input_device=device_id, min_db=-45)
        self.IntervalStream.start()

        self.frames = queue.Queue()

    def run(self):

        while self.running:

            self.update_bpm(self.IntervalStream.bpm)

            #print(self.bpm)

            if self.bpm > -1:
                #print(self.n)


                startTime = time.time()

                currentFrame = LayerHandler.combineLayers(self.layers,params={'n':self.n})
                #self.frames.put(LayerHandler.preprocess(currentFrame))
                #self.frames.put(LayerHandler.preprocess(LayerHandler.combineLayers(self.layers,params={'n':self.n})))
                print(currentFrame.shape)

                while self.IntervalStream.data_queue.qsize() > 0:
                    self.IntervalStream.data_queue.get()

                LayerHandler.Show(currentFrame, ftoi=True, cv2Show=True)

                if (self.n!=0) and (self.n%(self.resolution*2)==0):
                    self.layers = LayerHandler.randomLayers(self.possibleLayers, self.weights)
                    print(f"frame time: {self.frameTime}, meter length: {self.meter_length}, layers: {self.layers}")


                endTime = time.time()

                self.n+=1

                sleepTime = self.frameTime - (endTime - startTime)


                #print(f"sleep time: {sleepTime}")

                if cv2.waitKey(1) & 0xFF == ord( 'x' ):
                    break

                time.sleep(sleepTime if sleepTime > 0 else 0.01)

                #if cv2.waitKey(1) & 0xFF == ord( 'x' ):
                #    break
            else:

                self.layers = [FullColor(config={'color':(0,0,0,1.0)})]
                time.sleep(0.1)



    def update_bpm(self, bpm):
        self.bpm = bpm

        if self.bpm > -1:
            #1 frame per 1/16 measure (seconds/1/16measure)
            self.meter_length = 1/(bpm/60/4)
            self.frameTime = self.meter_length / self.resolution
        else:
            self.meter_length = 0
            self.frameTime = 0
