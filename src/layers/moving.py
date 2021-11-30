import cv2
import numpy as np
import math
from layers.layer import Layer

class Move(Layer):

    def compute(self, current=None, params={}):

        #horizontal direction ('left', 'right', or None)
        if 'horizontal' not in self.config:
            self.config['horizontal'] = None
        #vertical direction ('up', 'down', or None)
        if 'vertical' not in self.config:
            self.config['vertical'] = None
        #speed of movement (int)
        if 'speed' not in self.config:
            self.config['speed'] = 5


        if self.config['horizontal'] is not None:
            #movement index
            mi = self.config['speed'] * self.n_l
            if mi >= self.dims[0]:
                mi -= self.dims[0]
                self.n_l = 0


            if mi > 0:

                if self.config['horizontal'] == 'left':
                    temp = current[0:mi,:]
                    current[0:self.dims[0] - mi, :] = current[mi:self.dims[0],:]
                    current[self.dims[0] - mi:,:] = temp

                elif self.config['horizontal'] == 'right':
                    temp = current[self.dims[0] - mi:,:]
                    current[mi:self.dims[0],:] = current[0:self.dims[0] - mi, :]
                    current[0:mi,:] = temp


        if self.config['vertical'] is not None:
            #movement index
            mi = self.config['speed'] * self.n_l
            if mi >= self.dims[1]:
                mi -= self.dims[1]
                self.n_l = 0

            print(mi)

            if mi > 0:

                if self.config['vertical'] == 'up':
                    temp = current[:,0:mi]
                    current[:, 0:self.dims[1] - mi] = current[:, mi:self.dims[1]]
                    current[:, self.dims[1] - mi:] = temp

                elif self.config['vertical'] == 'down':
                    temp = current[:, self.dims[1] - mi:]
                    current[:, mi:self.dims[1]] = current[:, 0:self.dims[1] - mi]
                    current[:, 0:mi] = temp

        return current
