import cv2
import numpy as np
import math
from layers.layer import Layer

class Split4(Layer):

    def compute(self, current=None, params={}):

        quad = cv2.resize(current, dsize=(self.dims[1]//2,self.dims[0]//2), interpolation=cv2.INTER_CUBIC)

        current[0:self.dims[0]//2,0:self.dims[1]//2] = quad
        current[0:self.dims[0]//2,self.dims[1]//2:] = quad
        current[self.dims[0]//2:,0:self.dims[1]//2] = quad
        current[self.dims[0]//2:,self.dims[1]//2:] = quad

        return current
