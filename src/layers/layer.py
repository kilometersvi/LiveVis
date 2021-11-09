import cv2
from abc import ABC, abstractmethod

class LayerFrame:

    def __init__(self, layer):
        self.layer = layer


    def __add__(self, o):
        return layer.effect(o)

class Layer:

    def __init__(self, n=0):
        self.n = n
        self.frame =

    def __iter__(self):
        random.shuffle(self.all_data)
        batch = list()
        for i in self.all_data:
            batch.append(i)
            if len(batch) >= self.size:
                yield batch
                batch = list()

    def __call__(self, n):
        self.n = n
        return self

    def run(self):

    def effect(self, o):
        frame = cv2.addWeighted(self.frame,1,o.frame,1,0)
        return frame;
        #return self.a + o.a
