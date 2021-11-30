import cv2
import numpy as np
import math
from layers.layer import Layer

class ColorMix2Split(Layer):

    def compute(self, current=None, params={}):
        v1 = math.sin(self.n_l/10)
        v2 = math.cos(self.n_l/30)
        current[:,0:self.dims[1]//2] += (v1,0,0,0)      # (B, G, R)
        current[:,self.dims[1]//2:self.dims[1]] += (0,v2,0,0)


        return current
